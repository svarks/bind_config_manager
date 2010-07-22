import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

from pylons.decorators import rest
from bind_config_manager.model import meta, User
from bind_config_manager.forms.auth import SignUpForm
from pylons.decorators import validate
from formencode import htmlfill
import bind_config_manager.lib.helpers as h
import hashlib

class AuthController(BaseController):
  
  def sign_in(self):
    return render('/auth/sign_in.html')
  
  @rest.restrict("POST")
  def sign_in_submit(self):
    username = request.params['username']
    password = hashlib.sha1(request.params['password']).hexdigest()
    user = meta.Session.query(User).filter_by(username=username).first()
    
    if (user and user.password == password):
      if user.is_active == True:
        session["user"] = user
        session.save()
        h.flash('Logged in successfully.')
      else:
        h.flash('Please wait before your account will be activated.')
      redirect('/')
    else:
      h.flash('Username or password doesn\'t match.')
      return render('/auth/sign_in.html')
  
  def sign_up(self):
    return render('/auth/sign_up.html')
    
  @rest.restrict("POST")
  @validate(schema=SignUpForm(), form='sign_up')
  def sign_up_submit(self):
    username = request.params['username']
    password = hashlib.sha1(request.params['password']).hexdigest()
    user = User(username=username, password=password)
    meta.Session.add(user)
    meta.Session.commit()
    h.flash('You have successfully signed up.')
    redirect('/')
    
  def sign_out(self):
    session["user"] = None
    session.delete()
    h.flash("You have been logged out.")
    redirect('/')
