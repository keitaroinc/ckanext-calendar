import logging

from ckan.plugins import toolkit
from ckan import logic
import ckan.lib.navl.dictization_functions as df

from ckanext.calendar.logic import schema
from ckanext.calendar.model import ckanextEvent
from ckanext.calendar.logic.dictization import event_dictize

log = logging.getLogger(__name__)


def event_update(context, data_dict):
    '''Update an event. This will update all fields. See event_create for
    possible fields.

    :param id: The id of the event.
    :type id: string

    :returns: an updated event
    :rtype: dictionary

    '''

    log.info('Event update: %r', data_dict)

    logic.check_access('event_update', context, data_dict)

    event_update_schema = schema.event_update_schema()

    data, errors = df.validate(data_dict, event_update_schema,
                               context)

    if errors:
        raise toolkit.ValidationError(errors)

    event = ckanextEvent.get(key=data['id'], attr='id')

    if event is None:
        raise logic.NotFound

    event.title = data.get('title')
    event.start = data.get('start')
    event.end = data.get('end')
    event.description = data.get('description', u'')
    event.venue = data.get('venue', u'')
    event.meta = data.get('meta', u'{}')
    event.active = data.get('active', False)

    event.save()

    out = event_dictize(event)

    return out
