"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from bind_config_manager.model.meta import Session

from pylons import request, session, url
from pylons.controllers.util import redirect
import bind_config_manager.lib.helpers as h

class BaseController(WSGIController):
    
    requires_auth = False
    requires_admin = False
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __before__(self):
        # Authentication required?
        if (self.requires_auth or self.requires_admin) and 'user' not in session:
            # Remember where we came from so that the user can be sent there
            # after a successful login
            session['path_before_login'] = request.path_info
            session.save()
            h.flash('You have to sign up or sign in before access this page.')
            return redirect(url(controller='auth', action='sign_in'))
        if self.requires_admin:
            if 'user' not in session or session['user'].is_admin == False:
                h.flash("You don't have permissions to access this page.", 'warning')
                redirect('/')
                
