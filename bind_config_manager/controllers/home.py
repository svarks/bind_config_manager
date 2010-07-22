import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from bind_config_manager.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HomeController(BaseController):
    
    def index(self):
        return render('home/index.html')
    