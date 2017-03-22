import json
import logging

from ckan.lib import base
from ckan.plugins import toolkit
from ckan import model, logic
from ckan.common import c, _, request
import ckan.lib.helpers as h


log = logging.getLogger(__name__)


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

    def event_create(self, data=None):
        print 'INTO EVENT CREATE'
        log.debug(request.method)
        print request.GET
        if request.method.lower() == 'post':
            fields = {
                'title': request.POST['event-name'],
                'description': request.POST['event-description'],
                'start': request.POST['event-start-date'],
                'end': request.POST['event-end-date']
            }

            result = _get_action('event_create', fields)

            h.flash_notice(_('Event created'))
            return self.event_index()

        return toolkit.render('events/event_form.html', extra_vars={})

    def event_update(self, id):
        event = _get_action('event_show', {'id': id})
        extra_vars = {
            'event': event
        }

        if request.method.lower() == 'post':
            fields = {
                'id': id,
                'title': request.POST['event-name'],
                'description': request.POST['event-description'],
                'start': request.POST['event-start-date'],
                'end': request.POST['event-end-date']
            }

            result = _get_action('event_update', fields)

            print result
            h.flash_notice(_('Event updated'))
            return self.event_show(id)


        return toolkit.render('events/event_update.html', extra_vars)

    def event_delete(self, id):
        event = _get_action('event_delete', {'id': id})

        h.flash_notice(_('Event removed'))

        return self.event_show(id)
        