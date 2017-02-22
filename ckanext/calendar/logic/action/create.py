# -*- coding: utf-8 -

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

import logging

import ckan.logic as l
import ckan.plugins.toolkit as t
import ckan.lib.helpers as lh

from ckan.common import _
from ckanext.calendar.model import ckanextEvent, gen_event_name
from ckanext.calendar.logic.dictization import event_dictize

log = logging.getLogger(__name__)


def event_create(context, data_dict):
    '''Create an event.

    :param title: The title of the event.
    :type title: string

    :param description: Description of the event.
    :type description: string

    :param venue: Venue of the event.
    :type venue: string

    :param start: Start date of the event.
    :type start: string

    :param end: End date of the event.
    :type end: string

    :param meta: Additional meta data for the event such as latitude/longitude etc.
    :type meta: JSON

    :returns: the newly created event
    :rtype: dictionary

    '''
    log.info('Event create: %r', data_dict)

    l.check_access('event_create', context, data_dict)

    title = l.get_or_bust(data_dict, 'title')
    start = l.get_or_bust(data_dict, 'start')
    start = lh.date_str_to_datetime(start)
    name = gen_event_name(title)
    description = data_dict.get('description', '')
    venue = data_dict.get('venue', '')
    end = lh.date_str_to_datetime(
        data_dict.get('end', data_dict['start'])
    )
    meta = data_dict.get('meta', u'{}')


    m = context.get('model')
    user_obj = m.User.get(context.get('user'))

    event = ckanextEvent(title=title,
                         name=name,
                         description=description,
                         start=start,
                         end=end,
                         venue=venue,
                         meta=meta,
                         creator_id=user_obj.id)
    event.save()

    out = event_dictize(event)
    return out
