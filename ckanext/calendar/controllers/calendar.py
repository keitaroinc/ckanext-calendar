from ckan.lib import base
from ckan.plugins import toolkit
from ckan import model
from ckan.common import c


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
