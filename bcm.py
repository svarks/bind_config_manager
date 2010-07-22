#!/usr/bin/env python

import sys
import cmdln

# pylons project initialize
from paste.deploy import appconfig
from pylons import config
from bind_config_manager.config.environment import load_environment
conf = appconfig('config:development.ini', relative_to='.')
load_environment(conf.global_conf, conf.local_conf)
# loading models
from bind_config_manager.model import Base, Session, Domain, Record

class BindConfig(cmdln.Cmdln):
  name = "bcm"
  
  def do_domain_list(self, subcmd, opts, *args):
    domains = Session.query(Domain).all()
    for domain in domains:
      self._print_records(domain.type, domain.name)
  do_domain_list.__doc__ = "Display list of available domains."
  
  def do_domain_show(self, subcmd, opts, *args):
    domain = self._find_domain(args)
    if domain:
      print '\nDomain Information:'
      print '-------------------'
      self._print_records(domain.type, domain.name, domain.soa_nameserver, domain.admin_mailbox, domain.serial,
        domain.refresh_ttl, domain.retry_ttl, domain.expire_ttl, domain.minimum_ttl, domain.default_ttl
      )
      print '\nDomain Records:'
      print '---------------'
      for record in domain.records:
        self._print_records(record.id, record.type, record.ttl, (record.priority or ''), record.name, record.value)
    else:
      print 'Usage: domain_show <domain_name>'
  do_domain_show.__doc__ = "Show detailed information about specified domain."
  
  def do_domain_check(self, subcmd, opts, *args):
    domain = self._find_domain(args)
    if domain:
      print domain.get_server_response()
    else:
      print 'Usage: domain_check <domain_name>'
  do_domain_check.__doc__ = "Check response from DNS server."
  
  def do_domain_add(self, subcmd, opts, *args):
    if len(args) > 3:
      domain = Domain(*args)
      Session.add(domain)
      Session.commit()
    else:
      print 'Usage: domain_add <type> <name> <soa_nameserver> <admin_mailbox>'
  do_domain_add.__doc__ = "Add new domain."
  
  def do_domain_delete(self, subcmd, opts, *args):
    domain = self._find_domain(args)
    if domain:
      Session.delete(domain)
      Session.commit()
    else:
      print 'Usage: domain_delete <domain_name>'
  do_domain_delete.__doc__ = "Delete specified domain."
  
  def do_record_add(self, subcmd, opts, *args):
    domain = self._find_domain(args)
    if domain and len(args) > 3:
      record = Record(*args[1:])
      record.domain = domain
      Session.add(record)
      Session.commit()
    else:
      print 'Usage: record_add <domain_name> <record_type> <record_name> <record_value>'
  do_record_add.__doc__ = "Add new record into specified domain."
  
  def do_record_delete(self, subcmd, opts, *args):
    record = None
    if len(args) > 0:
      record = Session.query(record).filter_by(id=unicode(args[0])).first()
    if record:
      Session.delete(record)
      Session.commit()
    else:
      print 'Record not found.'
      print 'Usage: record_delete <record_id>'
  do_record_add.__doc__ = "Delete specified record."
  
  
  def _find_domain(self, args):
    domain = None
    if len(args) > 0:
      domain = Session.query(Domain).filter_by(name=unicode(args[0])).first()
    if not domain:
      print "Domain not found."
    return domain
  
  def _print_records(self, *records):
    for record in records:
      print '%s\t' % (record),
    print ''
  
if __name__ == "__main__":
  bc = BindConfig()
  sys.exit(bc.main())
