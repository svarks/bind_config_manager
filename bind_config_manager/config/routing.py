"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    
    map.resource("session", "sessions")
    map.resource("user", "users")
    map.resource("domain", "domains")
    map.resource('record', 'records', parent_resource=dict(member_name='domain', collection_name='domains'))
    map.resource("event", "events")
    
    map.connect('/', controller='home')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
