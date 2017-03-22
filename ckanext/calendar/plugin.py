import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.calendar.model import setup as model_setup
import ckanext.calendar.helpers as _h
import ckanext.calendar.logic.auth as pauth

from routes.mapper import SubMapper

log = logging.getLogger(__name__)


class CalendarPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IRoutes, inherit=True)

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

    # IRouter

    def before_map(self, map):

        ctrl = 'ckanext.calendar.controllers.calendar:CalendarController'
        with SubMapper(map, controller=ctrl) as m:
            m.connect('event_index', '/events', action='event_index')
            m.connect('event_create', '/events/create',
                        action='event_create')
            m.connect('event_show', '/events/{id}',
                        action='event_show')
            m.connect('event_update', '/events/update/{id}',
                        action='event_update')

        return map
