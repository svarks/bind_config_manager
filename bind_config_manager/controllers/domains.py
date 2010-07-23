import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

import bind_config_manager.lib.helpers as h
from bind_config_manager import model
from bind_config_manager.model import meta
from formalchemy import FieldSet

DomainFields = FieldSet(model.Domain)
DomainFields.configure(options=[DomainFields.type.dropdown(['master', 'slave'])], exclude=[DomainFields.records])

class DomainsController(BaseController):
    
    requires_auth = True
    
    def index(self):
        c.domains = meta.Session.query(model.Domain).all()
        return render('domains/index.html')
    
    def new(self):
        c.fs = DomainFields
        return render('domains/new.html')
    
    def create(self):
        domain = model.Domain()
        c.fs = DomainFields.bind(domain, data=request.POST)
        if c.fs.validate():
            c.fs.sync()
            meta.Session.add(domain)
            meta.Session.commit()
            h.flash('Domain created.')
            return redirect(url('domains'))
        else:
            return render('domains/new.html')
    
    def show(self, id):
        c.domain = meta.Session.query(model.Domain).filter_by(id=id).first()
        return render('domains/show.html')
    
    def edit(self, id, format='html'):
        c.domain = meta.Session.query(model.Domain).filter_by(id=id).first()
        c.fs = DomainFields.bind(c.domain)
        return render('domains/edit.html')
    
    def update(self, id):
        domain = meta.Session.query(model.Domain).filter_by(id=id).first()
        c.fs = DomainFields.bind(domain, data=request.POST)
        if c.fs.validate():
            c.fs.sync()
            meta.Session.commit()
            h.flash('Domain updated.')
            return redirect(url('domains'))
        else:
            return render('domains/edit.html')
    
    def delete(self, id):
        domain = meta.Session.query(model.Domain).filter_by(id=id).first()
        meta.Session.delete(domain)
        meta.Session.commit()
        h.flash('Domain deleted.')
        return redirect(url('domains'))
