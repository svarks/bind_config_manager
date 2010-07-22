"""Setup the bind_config_manager application"""
import logging

import pylons.test

from bind_config_manager.config.environment import load_environment
from bind_config_manager.model.meta import Session, Base

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup bind_config_manager here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)
    
    
    ####################
    # load initial data
    ####################
    
    from bind_config_manager.model import User, Domain, Record
    import hashlib
    
    Session.query(User).delete()
    Session.query(Record).delete()
    Session.query(Domain).delete()
    
    u = User(username='admin', password=hashlib.sha1('admin').hexdigest(), is_admin=True, is_active=True)
    Session.add(u)
    u = User(username='user', password=hashlib.sha1('user').hexdigest(), is_admin=False, is_active=True)
    Session.add(u)
    
    d = Domain('master', 'example.com', 'ns1.example.com', 'hostmaster.example.com')
    Session.add(d)
    Session.commit()
    Session.add_all([
      Record(d.id, 'NS',    '@',        'ns1.example.com'),
      Record(d.id, 'NS',    '@',        'ns2.example.com'),
      Record(d.id, 'A',     '@',        '192.168.10.10'),
      Record(d.id, 'A',     'ns1',      '192.168.1.10'),
      Record(d.id, 'A',     'ns2',      '192.168.1.20'),
      Record(d.id, 'A',     'mail',     '192.168.2.10', priority=10),
      Record(d.id, 'A',     'mail2',    '192.168.2.20', priority=20),
      Record(d.id, 'A',     'www2',     '192.168.10.20'),
      Record(d.id, 'CNAME', 'www',      '@'),
      Record(d.id, 'CNAME', 'ftp',      '@'),
      Record(d.id, 'CNAME', 'webmail',  '@'),
    ])
    
    d = Domain('master', '0.0.127.in-addr.arpa', 'ns1.linux.bogus', 'hostmaster.linux.bogus')
    Session.add(d)
    Session.commit()
    Session.add_all([
      Record(d.id, 'NS',    '@',        'ns.linux.bogus'),
      Record(d.id, 'PTR',   '1',        'localhost'),
    ])
    
    
    Session.commit()
    