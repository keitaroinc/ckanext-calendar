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

from ckan.plugins import toolkit as t
import ckanext.calendar.helpers as _h

log = logging.getLogger(__name__)


def event_create(context, data_dict):
    '''
        Authorization check for event creation
    '''
    success = _h.user_is_sysadmin(context)
    out = {
        'success': success,
        'msg': '' if success else
        t._('User {0} not authorized to create events')
    }
    return out


def event_update(context, data_dict):
    '''
        Authorization check for event update
    '''

    success = _h.user_is_sysadmin(context)
    out = {
        'success': success,
        'msg': '' if success else
        t._('User {0} not authorized to update events')
    }
    return out


def event_patch(context, data_dict):
    '''
        Authorization check for event patch
    '''

    success = _h.user_is_sysadmin(context)
    out = {
        'success': success,
        'msg': '' if success else
        t._('User {0} not authorized to patch events')
    }
    return out


def event_delete(context, data_dict):
    '''
        Authorization check for event delete
    '''
    success = _h.user_is_sysadmin(context)
    out = {
        'success': success,
        'msg': '' if success else
        t._('User {0} not authorized to delete events')
    }
    return out
