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
