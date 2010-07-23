import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

from pylons.decorators import rest

import bind_config_manager.lib.helpers as h
from bind_config_manager import model
from bind_config_manager.model import meta
from formalchemy import FieldSet

UserFields = FieldSet(model.User)
UserFields.configure(include=[UserFields.username, UserFields.password])
UserFields.password.name = 'password'

class AuthController(BaseController):
  
    def sign_in(self):
        c.fs = UserFields.bind(model.User)
        return render('/auth/sign_in.html')
  
    @rest.restrict("POST")
    def sign_in_submit(self):
        c.fs = UserFields.bind(model.User, data=request.POST)
        user = meta.Session.query(model.User).filter_by(username=c.fs.username.value).first()
        if (user and user.authenticate(c.fs.password.value)):
            if user.is_active == True:
                session["user"] = user
                session.save()
                h.flash('Logged in successfully.')
                if 'path_before_login' in session:
                    redirect(session['path_before_login'])
            else:
                h.flash('Please wait before your account will be activated.')
            redirect('/')
        else:
            h.flash('Username or password doesn\'t match.')
            return render('/auth/sign_in.html')
  
    def sign_up(self):
        c.fs = UserFields.bind(model.User)
        return render('/auth/sign_up.html')
    
    @rest.restrict("POST")
    def sign_up_submit(self):
        user = model.User()
        c.fs = UserFields.bind(user, data=request.POST)
        if c.fs.validate():
            c.fs.sync()
            meta.Session.add(user)
            meta.Session.commit()
            meta.Session.commit()
            h.flash('You have successfully signed up.')
            redirect('/')
        else:
            return render('/auth/sign_up.html')
    
    def sign_out(self):
        session["user"] = None
        session.delete()
        h.flash("You have been logged out.")
        redirect('/')
