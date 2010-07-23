import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

import bind_config_manager.lib.helpers as h
from bind_config_manager import model
from bind_config_manager.model import meta
from formalchemy import FieldSet

RecordFields = FieldSet(model.Record)
RecordFields.configure(
  options=[RecordFields.type.dropdown(['A', 'CNAME', 'MX', 'NS', 'PTR']), RecordFields.priority.label('Priority (for MX only)')],
  exclude=[RecordFields.domain]
)

class RecordsController(BaseController):
    
    requires_auth = True
    
    def __before__(self, action, domain_id=None):
        c.domain = meta.Session.query(model.Domain).filter_by(id=domain_id).first()
        BaseController.__before__(self)
    
    def new(self, domain_id):
        c.fs = RecordFields.bind(model.Record)
        return render('records/new.html')
    
    def create(self):
        record = model.Record()
        c.fs = RecordFields.bind(record, data=request.POST)
        if c.fs.validate():
            c.fs.sync()
            record.domain_id = c.domain.id
            meta.Session.add(record)
            meta.Session.commit()
            h.flash('Record created.')
            return redirect(url('domain', id=c.domain.id))
        else:
            return render('records/new.html')
    
    def edit(self, id, format='html'):
        record = meta.Session.query(model.Record).filter_by(id=id).first()
        c.fs = RecordFields.bind(record)
        return render('records/edit.html')
    
    def update(self, id):
        record = meta.Session.query(model.Record).filter_by(id=id, domain_id=c.domain.id).first()
        c.fs = RecordFields.bind(record, data=request.POST)
        if c.fs.validate():
            c.fs.sync()
            meta.Session.commit()
            h.flash('Record updated.')
            return redirect(url('domain', id=c.domain.id))
        else:
            return render('records/edit.html')
    
    def delete(self, id):
        record = meta.Session.query(Record).filter_by(id=id, domain_id=c.domain.id).first()
        meta.Session.delete(record)
        meta.Session.commit()
        h.flash('Record deleted.')
        return redirect(url('domain', id=c.domain.id))

