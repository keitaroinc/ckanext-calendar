import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.calendar.model import setup as model_setup
import ckanext.calendar.helpers as _h
import ckanext.calendar.logic.auth as pauth

from routes.mapper import SubMapper

try:
    # CKAN 2.7 and later
    from ckan.common import config as _config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config as _config

log = logging.getLogger(__name__)


class CalendarPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    startup = False

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'calendar')

    def get_auth_functions(self):
        return {
            'event_create': pauth.event_create,
            'event_update': pauth.event_update,
            'event_patch': pauth.event_patch,
            'event_delete': pauth.event_delete
        }

    # IConfigurable

    def configure(self, config):
        self.startup = True

        # Setup calendar model
        model_setup()

        self.startup = False

    # IActions

    def get_actions(self):
        module_root = 'ckanext.calendar.logic.action'
        action_functions = _h._scan_functions(module_root)
        return action_functions

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'calendar_get_current_url': _h.calendar_get_current_url,
            'calendar_get_recent_events': _h.calendar_get_recent_events,
            'calendar_truncate_limit': lambda: _config.get('ckanext.calendar.truncate_limit', 100)
        }

    # IRouter

    def before_map(self, map):
        ctrl = 'ckanext.calendar.controllers.calendar:CalendarController'
        with SubMapper(map, controller=ctrl) as m:
            m.connect('event_index', '/events', action='event_index')
            m.connect('event_create', '/events/create',
                      action='event_create')
            m.connect('event_delete', '/events/delete/{id}',
                      action='event_delete')
            m.connect('event_show', '/events/{id}',
                      action='event_show')
            m.connect('event_update', '/events/update/{id}',
                      action='event_update')

        return map
