import json

from ckan.lib import base
from ckan.plugins import toolkit
from ckan import model, logic
from ckan.common import c, _


def _get_context():
    return {
        'model': model,
        'session': model.Session,
        'user': c.user or c.author,
        'auth_user_obj': c.userobj
    }


def _get_action(action, data_dict):
    return toolkit.get_action(action)(_get_context(), data_dict)


class CalendarController(base.BaseController):

    def event_index(self):
        events = _get_action('event_list', {'limit': 100})

        extra_vars = {
            'events': events
        }

        return toolkit.render('events/events_list.html', extra_vars)

    def event_show(self, id):
        try:
            event = _get_action('event_show', {'id': id})
        except (logic.ValidationError, logic.NotFound):
            toolkit.abort(404, _('Event not found'))

        extra_vars = {
            'event': event
        }

        return toolkit.render('events/event_page.html', extra_vars)

    def event_create(self):

        # TODO implement functionality

        extra_vars = {
            'events': []
        }

        return toolkit.render('events/events_list.html', extra_vars)