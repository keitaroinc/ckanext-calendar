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

import logging

from ckan.plugins import toolkit
from ckan import logic
import ckan.lib.navl.dictization_functions as df

from ckanext.calendar.logic import schema
from ckanext.calendar.model import ckanextEvent
from ckanext.calendar.logic.dictization import event_dictize

log = logging.getLogger(__name__)


def event_patch(context, data_dict):
    '''Patch an event. See event_create for
    possible fields.

    The difference between the update and patch methods is that the patch will
    perform an update of the provided parameters, while leaving all other
    parameters unchanged, whereas the update method deletes all parameters
    not explicitly provided in the data_dict

    :param id: The id of the event.
    :type id: string

    :returns: a patched event
    :rtype: dictionary

    '''

    log.info('Event patch: %r', data_dict)

    logic.check_access('event_patch', context, data_dict)

    event_patch_schema = schema.event_patch_schema()
    fields = event_patch_schema.keys()

    # Exclude fields from the schema that are not in data_dict
    for field in fields:
        if field not in data_dict.keys() and field != 'id':
            event_patch_schema.pop(field)

    data, errors = df.validate(data_dict, event_patch_schema,
                               context)

    if errors:
        raise toolkit.ValidationError(errors)

    event = ckanextEvent.get(key=data['id'], attr='id')

    if event is None:
        raise logic.NotFound

    fields = event_patch_schema.keys()

    for field in fields:
        setattr(event, field, data.get(field))

    event.save()

    out = event_dictize(event)

    return out
