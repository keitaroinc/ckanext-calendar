import logging

from ckan import logic
from ckan.plugins import toolkit

from ckanext.calendar.model import ckanextEvent

log = logging.getLogger(__name__)


def event_delete(context, data_dict):
    '''Delete event.

    :param id: the id of event
    :type id: string

    :rtype: dictionary

    '''

    logic.check_access('event_delete', context, data_dict)

    id = toolkit.get_or_bust(data_dict, 'id')

    event = ckanextEvent.delete(id=id)

    if event == 0:
        raise logic.NotFound
    
    log.info('Event delete: %r', data_dict)
    return {
        'message': 'Event successfully deleted'
    }
