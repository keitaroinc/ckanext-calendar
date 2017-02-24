import logging

log = logging.getLogger(__name__)


from ckan.plugins import toolkit as t
import ckanext.calendar.helpers as _h


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


def event_show(context, data_dict):
    return {
        'success': True
    }


def event_list(context, data_dict):
    return {
        'success': True
    }
