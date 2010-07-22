import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

from bind_config_manager.model import meta, Domain, Record
from bind_config_manager.forms.records import RecordForm
from pylons.decorators import validate
from formencode import htmlfill

class RecordsController(BaseController):
    
    requires_auth = True
    
    def __before__(self, action, domain_id=None):
        c.domain = meta.Session.query(Domain).filter_by(id=domain_id).first()
        BaseController.__before__(self)
    
    @validate(schema=RecordForm(), form='new')
    def create(self):
        record = Record()
        for k, v in self.form_result.items():
            setattr(record, k, v)
        record.domain_id = c.domain.id
        # c.domain.records.append(record)
        meta.Session.add(record)
        meta.Session.commit()
        return redirect(url('domain', id=c.domain.id))

    def new(self, domain_id):
        return render('records/new.html')
    
    @validate(schema=RecordForm(), form='edit')
    def update(self, id):
        record = meta.Session.query(Record).filter_by(id=id, domain_id=c.domain.id).first()
        for k,v in self.form_result.items():
            if getattr(record, k) != v:
                setattr(record, k, v)
        meta.Session.commit()
        return redirect(url('domain', id=c.domain.id))

    def delete(self, id):
        record = meta.Session.query(Record).filter_by(id=id, domain_id=c.domain.id).first()
        meta.Session.delete(record)
        meta.Session.commit()
        return redirect(url('domain', id=c.domain.id))

    def show(self, id):
        c.record = meta.Session.query(Record).filter_by(id=id).first()
        return render('records/show.html')

    def edit(self, id, format='html'):
        c.record = meta.Session.query(Record).filter_by(id=id).first()
        values = c.record.__dict__
        values['_method'] = 'put'
        return htmlfill.render(render('records/edit.html'), values)
