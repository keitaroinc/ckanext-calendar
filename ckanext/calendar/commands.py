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

import sys
from pprint import pprint

from ckan import model
from ckan.logic import get_action, ValidationError
from ckan.plugins import toolkit

from ckan.lib.cli import CkanCommand


class Calendar(CkanCommand):
    '''Enables management of events in CKAN
    Usage:
      harvester initdb
        - Creates the necessary tables in the database

    The commands should be run from the ckanext-calendar directory and expect
    a development.ini file to be present. Most of the time you will
    specify the config explicitly though::
        paster calendar initdb --config=../ckan/development.ini
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 9
    min_args = 0

    def __init__(self, name):
        super(Calendar, self).__init__(name)


    def command(self):
        self._load_config()

        # We'll need a sysadmin user to perform most of the actions
        # We will use the sysadmin site user (named as the site_id)
        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        self.admin_user = get_action('get_site_user')(context, {})

        print ''

        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)
        cmd = self.args[0]
        if cmd == 'initdb':
            self.initdb()
        else:
            print 'Command %s not recognized' % cmd

    def _load_config(self):
        super(Calendar, self)._load_config()

    def initdb(self):
        from ckanext.calendar.model import setup as db_setup
        db_setup()
        print 'Calendar DB tables created'