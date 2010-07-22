import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

from bind_config_manager.model import meta, User
from bind_config_manager.forms.auth import UserForm
from pylons.decorators import validate
from formencode import htmlfill
import bind_config_manager.lib.helpers as h

class UsersController(BaseController):
    
    def __before__(self):
        if (not 'user' in session) or session['user'].is_admin == False:
            h.flash("Access denied.")
            redirect('/')
    
    def index(self):
        c.users = meta.Session.query(User).all()
        return render('users/index.html')
    
    def edit(self, id, format='html'):
        c.user = meta.Session.query(User).filter_by(id=id).first()
        return render('users/edit.html')
    
    @validate(schema=UserForm(), form='edit')
    def update(self, id):
        domain = meta.Session.query(Domain).filter_by(id=id).first()
        for k,v in self.form_result.items():
            if getattr(domain, k) != v:
                setattr(domain, k, v)
        meta.Session.commit()
        return redirect(url('users'))

    def delete(self, id):
        user = meta.Session.query(User).filter_by(id=id).first()
        meta.Session.delete(user)
        meta.Session.commit()
        return redirect(url('users'))
