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

# -*- coding: utf-8 -
import logging
import uuid
import ckan.model as m
import ckanext.calendar.model as cm
import ckan.lib.helpers as h
from urllib import urlencode

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

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


def calendar_get_current_url(page, params, controller, action, exclude_param=''):
    url = h.url_for(controller=controller, action=action)
    for k, v in params:
        if k == exclude_param:
            params.remove((k, v))

    params = [(k, v.encode('utf-8') if isinstance(v, basestring) else str(v))
              for k, v in params]

    url = url + u'?page=' + str(page)
    if (params):
        url = url + u'?page=' + str(page) + '&' + urlencode(params)

    return url


def calendar_get_recent_events():
    limit = int(config.get('ckanext.calendar.recent_events_limit', 5))
    _ = m.Session.query(cm.ckanextEvent) \
        .order_by(cm.ckanextEvent.created_at.desc()) \
        .limit(limit).all()
    return _
