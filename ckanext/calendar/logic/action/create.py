# -*- coding: utf-8 -
"""
Copyright (c) 2017 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

import logging

import ckan.logic as l
import ckan.plugins.toolkit as t
import ckan.lib.navl.dictization_functions as df

from ckan.common import _
from ckanext.calendar.model import ckanextEvent, gen_event_name
from ckanext.calendar.logic.dictization import event_dictize
from ckanext.calendar.logic import schema

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

    :param active: State of the event (optional). Default is true.
    :type active: boolean

    :param meta: Additional meta data for the event such as latitude/longitude etc.
    :type meta: string in JSON format

    :returns: the newly created event
    :rtype: dictionary

    '''

    log.info('Event create: %r', data_dict)

    l.check_access('event_create', context, data_dict)

    data, errors = df.validate(data_dict, schema.event_create_schema(),
                               context)

    if errors:
        raise t.ValidationError(errors)

    title = data.get('title')
    name = gen_event_name(title)
    start = data.get('start')
    end = data.get('end')
    description = data.get('description', u'')
    venue = data.get('venue', u'')
    meta = data.get('meta', u'{}')
    active = data.get('active', False)

    m = context.get('model')
    user_obj = m.User.get(context.get('user'))

    event = ckanextEvent(title=title,
                         name=name,
                         description=description,
                         start=start,
                         end=end,
                         venue=venue,
                         meta=meta,
                         active=active,
                         creator_id=user_obj.id)
    event.save()

    out = event_dictize(event)
    return out
