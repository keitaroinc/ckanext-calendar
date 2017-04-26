import logging

from ckan import logic
from ckan.plugins import toolkit

from ckanext.calendar.model import ckanextEvent
from ckanext.calendar.logic.dictization import (
    event_dictize,
    event_list_dictize
)
from datetime import datetime

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def event_show(context, data_dict):
    '''Return the metadata of an event.

    :param id: the id of the event
    :type id: string

    :rtype: dictionary

    '''
    log.info('Event show: %r', data_dict)

    id = toolkit.get_or_bust(data_dict, 'id')

    event = ckanextEvent.get(key=id, attr='id')

    if event is None:
        raise logic.NotFound

    out = event_dictize(event)

    return out


@toolkit.side_effect_free
def event_list(context, data_dict):
    '''Return a list of created events ordered by date of creation (DESC) (defaults to 5).

    :param limit: limit the number of events to return (optional)
    :type id: int
    :param offset: offset  the results (defaults to 0)
    :type id: int

    :rtype: list of dictionaries

    '''
    log.info('Event list: %r', data_dict)

    limit = data_dict.get('limit', 5)
    offset = data_dict.get('offset', 0)
    future = data_dict.get('future_events', False)
    
    if future:
        event_list = context['session'].query(ckanextEvent)\
                        .filter(ckanextEvent.start >= datetime.utcnow())\
                        .order_by(ckanextEvent.created_at.desc()) \
                        .limit(limit).offset(offset).all()
    else:
        event_list = ckanextEvent.search(limit=limit, offset=offset, order='created_at desc')

    cnt = context['session'].query(ckanextEvent).count()

    # TODO: Update tests
    out = {}
    out['events'] = event_list_dictize(event_list)
    out['count'] = cnt


    return out
