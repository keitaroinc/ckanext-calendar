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

import ckan.model as m


def event_dictize(obj):
    out = obj.as_dict()

    creator = m.User.get(out['creator_id'])
    out['creator'] = creator.name
    del out['creator_id']
    return out


def event_list_dictize(list_of_dict):
    event_list = []

    for obj in list_of_dict:
        event_list.append(event_dictize(obj))

    return event_list
