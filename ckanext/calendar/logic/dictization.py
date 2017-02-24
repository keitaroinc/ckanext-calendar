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
