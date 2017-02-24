import logging

from ckan import logic
from ckan.plugins import toolkit

from ckanext.calendar.model import ckanextEvent
from ckanext.calendar.logic.dictization import event_dictize, event_list_dictize

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def event_show(context, data_dict):
    '''Return the metadata of an event.

    :param id: the id or name of the dataset
    :type id: string

    '''
    log.info('Event show: %r', data_dict)

    logic.check_access('event_show', context, data_dict)

    id = data_dict.get('id')

    event = ckanextEvent.get(key=id, attr='id')

    if event is None:
        raise logic.NotFound

    out = event_dictize(event)

    return out


@toolkit.side_effect_free
def event_list(context, data_dict):
    '''Return a list of last created events (defaults to 5).

    :param limit: limit the number of events to return
    :type id: int

    :rtype: list of dicts

    '''
    log.info('Event show: %r', data_dict)

    logic.check_access('event_list', context, data_dict)

    limit = data_dict.get('limit')

    if limit is None:
        limit = 5

    event_list = ckanextEvent.search(limit=limit, order='created_at desc')

    out = event_list_dictize(event_list)

    return out
