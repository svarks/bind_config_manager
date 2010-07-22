"""The application's model objects"""
from bind_config_manager.model.meta import Session, Base


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

import sqlalchemy as sa
import os
import dns.zone
import dns.rdatatype
import dns.rdataclass
import datetime
import re
from time import time
from pylons import session
from pylons import config

class User(Base):
  __tablename__ = 'users'
  
  id        = sa.Column(sa.types.Integer, primary_key=True)
  username  = sa.Column(sa.types.Unicode)
  password  = sa.Column(sa.types.Unicode)
  is_admin  = sa.Column(sa.types.Boolean, default=False)
  is_active = sa.Column(sa.types.Boolean, default=False)
  
  def __str__(self):
    return self.username

class Event(Base):
  __tablename__ = 'events'

  id          = sa.Column(sa.types.Integer, primary_key=True)
  target_id   = sa.Column(sa.types.Integer)
  action      = sa.Column(sa.types.Unicode)
  user_id     = sa.Column(sa.types.Integer, sa.ForeignKey('users.id'))
  user        = sa.orm.relation(User)
  created_at  = sa.Column(sa.types.DateTime, default=datetime.datetime.now)
  
  def target(self):
    if re.match(r'domain', self.action):
      return Session.query(Domain).filter_by(id=self.target_id).first()
    if re.match(r'record', self.action):
      return Session.query(Record).filter_by(id=self.target_id).first()
    return None

class DomainCallbacks(sa.orm.interfaces.MapperExtension):
  def after_insert(self, mapper, connection, instance):
    # print "<<<<<<<<<<<<<<< Domain insert"
    instance.update_zones_config()
    instance.write_zone_file()
    self._add_event(instance, 'insert')
  def after_update(self, mapper, connection, instance):
    # print "<<<<<<<<<<<<<<< Domain update"
    instance.update_zones_config()
    instance.write_zone_file()
    self._add_event(instance, 'update')
  def after_delete(self, mapper, connection, instance):
    # print "<<<<<<<<<<<<<<< Domain delete"
    instance.update_zones_config()
    instance.delete_zone_file()
    self._add_event(instance, 'delete')
  def _add_event(self, instance, action):
    event = Event(target_id=instance.id, action='domain_'+action)
    try:
      event.user_id = session['user'].id
    except:
      pass
    Session.add(event)

class RecordCallbacks(sa.orm.interfaces.MapperExtension):
  def after_insert(self, mapper, connection, instance):
    self._write_domain_zone(instance.domain_id)
    self._add_event(instance, 'insert')
  def after_update(self, mapper, connection, instance):
    self._write_domain_zone(instance.domain_id)
    self._add_event(instance, 'update')
  def after_delete(self, mapper, connection, instance):
    self._write_domain_zone(instance.domain_id)
    self._add_event(instance, 'delete')
  def before_insert(self, mapper, connection, instance):
    domain = self._find_domain(instance.domain_id)
    if instance.ttl == None:
      if domain:
        instance.ttl = domain.default_ttl
    if instance.type != 'MX':
      instance.priority = None
      
  def _add_event(self, instance, action):
    event = Event(target_id=instance.id, action='record_'+action)
    try:
      event.user_id = session['user'].id
    except:
      pass
    Session.add(event)
  def _find_domain(self, id):
    return Session.query(Domain).filter_by(id=id).first()
  def _write_domain_zone(self, domain_id):
    domain = self._find_domain(domain_id)
    if domain:
      domain.write_zone_file()

class Record(Base):
  __tablename__ = 'records'
  __mapper_args__ = {'extension': RecordCallbacks()}
  
  id        = sa.Column(sa.types.Integer, primary_key=True)
  domain_id = sa.Column(sa.types.Integer, sa.ForeignKey('domains.id'))
  type      = sa.Column(sa.types.Unicode)
  name      = sa.Column(sa.types.Unicode)
  value     = sa.Column(sa.types.Unicode)
  priority  = sa.Column(sa.types.Integer)
  ttl       = sa.Column(sa.types.Integer, default=3600)
  
  def __init__(self, domain_id=None, type=None, name=None, value=None, ttl=None, priority=None):
    self.domain_id = domain_id
    self.type = type
    self.name = name
    self.value = value
    self.ttl = ttl
    self.priority = priority
  
class Domain(Base):
  __tablename__ = 'domains'
  __mapper_args__ = {'extension': DomainCallbacks()}
  
  id              = sa.Column(sa.types.Integer, primary_key=True)
  type            = sa.Column(sa.types.Unicode)
  name            = sa.Column(sa.types.Unicode)
  soa_nameserver  = sa.Column(sa.types.Unicode)
  admin_mailbox   = sa.Column(sa.types.Unicode)
  serial          = sa.Column(sa.types.Integer, default=int(time()))
  refresh_ttl     = sa.Column(sa.types.Integer, default=28800)
  retry_ttl       = sa.Column(sa.types.Integer, default=14400)
  expire_ttl      = sa.Column(sa.types.Integer, default=3600000)
  minimum_ttl     = sa.Column(sa.types.Integer, default=86400)
  default_ttl     = sa.Column(sa.types.Integer, default=86400)
  records         = sa.orm.relation(Record, backref='domain', cascade='all')
  
  def __init__(self, type=None, name=None, soa_nameserver=None, admin_mailbox=None):
    self.type = type
    self.name = name
    self.soa_nameserver = soa_nameserver
    self.admin_mailbox = admin_mailbox
  
  def update_zones_config(self):
    f = open(config['named.zones_config'], "w")
    for domain in Session.query(Domain).all():
      text = "zone " + domain.name + " {\n"
      text += "  type " + domain.type + ";\n"
      text += "  file \"zones/" + domain.name + "\";\n"
      text += "};\n\n"
      f.write(text)
    f.close()
    
  def zone_file_name(self):
    return config['named.zones_dir'] + '/' + self.name
  
  def write_zone_file(self):
    z = dns.zone.Zone(dns.name.from_text(self.name))
    soa = dns.rdataset.from_text('IN', 'SOA', self.default_ttl, " ".join([
      str(self.soa_nameserver),
      str(self.admin_mailbox),
      str(self.serial),
      str(self.refresh_ttl),
      str(self.retry_ttl),
      str(self.expire_ttl),
      str(self.minimum_ttl),
    ]))
    node = z.find_node('@', True)
    node.rdatasets.append(soa)
    
    for record in self.records:
      rds = dns.rdataset.from_text('IN', str(record.type), int(record.ttl), str(record.value))
      node = z.find_node(record.name, True)
      node.rdatasets.append(rds)
    
    z.to_file(self.zone_file_name())
  
  def delete_zone_file(self):
    os.remove(self.zone_file_name())
  