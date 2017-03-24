import json
import logging

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

from ckan.lib import base
from ckan.plugins import toolkit
from ckan import model, logic
from ckan.common import c, _, request
import ckan.lib.helpers as h
import ckan.plugins as p


log = logging.getLogger(__name__)
redirect = base.redirect


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

    def __get_page_number(self, params):
        if p.toolkit.check_ckan_version(min_version='2.5.0', max_version='2.5.10'):
            return self._get_page_number(params)
        return h.get_page_number(params)

    def event_index(self):
        # TODO: Handle errors
        page = self.__get_page_number(request.params)
        limit = int(config.get('ckanext.calendar.events_show_limit', 3))
        pagination_limit = int(config.get('ckanext.calendar.pagination_limit', 3))
        c.page = page
        c.limit = limit
        c.pagination_limit = pagination_limit
        offset = (page - 1) * limit if page > 1 else 0
        data = _get_action('event_list', {'limit': limit, 'offset': offset })
        log.debug(data)
        c.total = data['count']
        extra_vars = {
            'events': data['events']
        }

        return toolkit.render('events/events_list.html', extra_vars)

    def event_show(self, id):
        # TODO: Handle errors
        try:
            event = _get_action('event_show', {'id': id})
        except (logic.ValidationError, logic.NotFound):
            toolkit.abort(404, _('Event not found'))

        extra_vars = {
            'event': event
        }
        return toolkit.render('events/event_page.html', extra_vars)

    def event_create(self, data=None):
        # TODO: Handle errors
        if request.method.lower() == 'post':
            fields = {
                'title': request.POST['event-name'],
                'description': request.POST['event-description'],
                'start': request.POST['add-event-start-date-input'],
                'end': request.POST['add-event-end-date-input'],
                'venue': request.POST['event-venue']
            }
            _get_action('event_create', fields)
            h.flash_success(_('The event was created successfully.'))
            redirect(h.url_for('event_index'))

        return toolkit.render('events/event_form.html', extra_vars={})

    def event_update(self, id):
        # TODO: Handle errors
        event = _get_action('event_show', {'id': id})
        extra_vars = {
            'event': event
        }
        if request.method.lower() == 'post':
            fields = {
                'title': request.POST['event-name'],
                'description': request.POST['event-description'],
                'start': request.POST['add-event-start-date-input'],
                'end': request.POST['add-event-end-date-input'],
                'venue': request.POST['event-venue'],
                'id':id
            }
            _get_action('event_update', fields)
            h.flash_success(_('The event was updated successfully.'))
            redirect(h.url_for('event_show', id=id))

        return toolkit.render('events/event_update.html', extra_vars)

    def event_delete(self, id):
        # TODO: Handle errors
        _get_action('event_delete', {'id': id})
        h.flash_success(_('The event was removed successfully.'))
        redirect(h.url_for('event_index'))
        