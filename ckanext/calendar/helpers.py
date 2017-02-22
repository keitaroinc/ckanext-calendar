# -*- coding: utf-8 -
import logging
import uuid
import ckan.model as m
import ckanext.calendar.model as cm

log = logging.getLogger(__name__)




def _scan_functions(module_root, _functions={}):
    '''Helper function that scans extension for all logic/auth functions.'''
    for module_name in ['create', 'delete', 'get', 'patch', 'update']:
        module_path = '%s.%s' % (module_root, module_name,)

        module = __import__(module_path)

        for part in module_path.split('.')[1:]:
            module = getattr(module, part)

        for key, value in module.__dict__.items():
            if not key.startswith('_') and (hasattr(value, '__call__')
                                            and (value.__module__ == module_path)):
                _functions[key] = value
    log.debug('SCANNED FUNCS')
    log.debug(_functions)
    return _functions

def user_is_sysadmin(context):
    '''
        Checks if the user defined in the context is a sysadmin
        rtype: boolean
    '''
    model = context['model']
    user = context['user']
    user_obj = model.User.get(user)
    if not user_obj:
        log.error('User {0} not found').format(user)
        return False

    return user_obj.sysadmin
