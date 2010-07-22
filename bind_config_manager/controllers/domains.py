import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

from bind_config_manager.model import meta, Domain
from bind_config_manager.forms.domains import DomainForm
from pylons.decorators import validate
from formencode import htmlfill

class DomainsController(BaseController):
    
    requires_auth = True
    
    def index(self):
        c.domains = meta.Session.query(Domain).all()
        return render('domains/index.html')
    
    @validate(schema=DomainForm(), form='new')
    def create(self):
        domain = Domain()
        for k, v in self.form_result.items():
            setattr(domain, k, v)
        meta.Session.add(domain)
        meta.Session.commit()
        return redirect('domains')

    def new(self):
        return render('domains/new.html')
    
    @validate(schema=DomainForm(), form='edit')
    def update(self, id):
        domain = meta.Session.query(Domain).filter_by(id=id).first()
        for k,v in self.form_result.items():
            if getattr(domain, k) != v:
                setattr(domain, k, v)
        meta.Session.commit()
        return redirect(url('domains'))

    def delete(self, id):
        domain = meta.Session.query(Domain).filter_by(id=id).first()
        meta.Session.delete(domain)
        meta.Session.commit()
        return redirect(url('domains'))

    def show(self, id):
        c.domain = meta.Session.query(Domain).filter_by(id=id).first()
        return render('domains/show.html')

    def edit(self, id, format='html'):
        c.domain = meta.Session.query(Domain).filter_by(id=id).first()
        values = c.domain.__dict__
        values['_method'] = 'put'
        return htmlfill.render(render('domains/edit.html'), values)
        # return render('domains/edit.html')
