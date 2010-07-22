import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

from bind_config_manager.model import meta, Event, User

class EventsController(BaseController):
    
    requires_auth = True
    
    def __before__(self):
        if (not 'user' in session) or session['user'].is_admin == False:
            h.flash("Access denied.")
            redirect('/')
    
    def index(self):
        query = meta.Session.query(Event)
        
        if 'action' in request.params and request.params['action']:
          query = query.filter_by(action=request.params['action'])
        if 'user' in request.params and request.params['user']:
          query = query.filter_by(user_id=request.params['user'])
        if 'date_from' in request.params and request.params['date_from']:
          query = query.filter(Event.created_at >= request.params['date_from'])
        if 'date_to' in request.params and request.params['date_to']:
          query = query.filter(Event.created_at <= request.params['date_to'])
          
        c.events = query.order_by('created_at desc').all()
        c.users = meta.Session.query(User).all()
        return render('events/index.html')
    