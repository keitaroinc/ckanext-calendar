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

from ckan.plugins import toolkit
import ckan.lib.helpers as h
import logging
from datetime import datetime

log = logging.getLogger(__name__)

not_empty = toolkit.get_validator('not_empty')
ignore_missing = toolkit.get_validator('ignore_missing')
not_missing = toolkit.get_validator('not_missing')
isodate = toolkit.get_validator('isodate')
boolean_validator = toolkit.get_validator('boolean_validator')


def event_create_schema():
    return {
        'title': [not_empty, unicode],
        'description': [ignore_missing, unicode],
        'venue': [ignore_missing, unicode],
        'start': [not_empty, start_is_not_in_past],
        'end': [not_empty, end_is_biger_than_start],
        'meta': [ignore_missing, unicode],
        'active': [ignore_missing, boolean_validator]
    }


def event_update_schema():
    schema = event_create_schema()
    schema['id'] = [not_empty, unicode]
    return schema


def event_patch_schema():
    return event_update_schema()


def start_is_not_in_past(key, data, errors, context):
    start = data.get(key)
    if isinstance(start, basestring):
        try:
            start = datetime.strptime(start, '%Y-%m-%d')
            if start.date() < datetime.utcnow().date():
                errors[key].append(toolkit._('Start date is in the past'))
        except ValueError:
            errors[key].append(toolkit._('Incorrect start date format, should be YYYY-MM-DD'))
    else:
        if start.date() < datetime.utcnow().date():
            errors[key].append(toolkit._('Start date can not be in past!'))


def end_is_biger_than_start(key, data, errors, context):
    end = data.get(key)
    start = data.get(('start',))

    if isinstance(start, basestring):
        try:
            start = datetime.strptime(start, '%Y-%m-%d')
        except ValueError:
            pass

    if isinstance(end, basestring):
        try:
            end = datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            errors[key].append(toolkit._('Incorrect end date format, should be YYYY-MM-DD'))

    if isinstance(start, datetime) and isinstance(end, datetime):
        if start.date() > end.date():
            errors[key].append(toolkit._('Incorect end date, should be greater than start date'))


