import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

from bind_config_manager import model
from bind_config_manager.model import meta
import bind_config_manager.lib.helpers as h

import formalchemy
from formalchemy import FieldSet

UserFields = FieldSet(model.User)
UserFields.configure(include=[UserFields.username, UserFields.password, UserFields.is_admin, UserFields.is_active])
UserFields.password.name = 'password'

class UsersController(BaseController):
    
    requires_admin = True
    
    def new(self):
        c.fs = UserFields
        return render('users/new.html')
    
    def create(self):
        user = model.User()
        c.fs = UserFields.bind(user, data=request.POST)
        if c.fs.validate():
            c.fs.sync()
            meta.Session.add(user)
            meta.Session.commit()
            h.flash('User created.')
            return redirect(url('users'))
        else:
            return render('users/new.html')
    
    def index(self):
        c.users = meta.Session.query(model.User).all()
        return render('users/index.html')
    
    def edit(self, id, format='html'):
        user = meta.Session.query(model.User).filter_by(id=id).first()
        user.encrypted_password = ''
        c.fs = UserFields.bind(user)
        return render('users/edit.html')
    
    def update(self, id):
        user = meta.Session.query(model.User).filter_by(id=id).first()
        c.fs = UserFields.bind(user, data=request.POST)
        c.fs.password.validators.remove(formalchemy.validators.required)
        if c.fs.validate():
            c.fs.sync()
            meta.Session.commit()
            h.flash('User updated.')
            return redirect(url('users'))
        else:
            return render('users/edit.html')
    
    def delete(self, id):
        user = meta.Session.query(model.User).filter_by(id=id).first()
        meta.Session.delete(user)
        meta.Session.commit()
        h.flash('User deleted.')
        return redirect(url('users'))
