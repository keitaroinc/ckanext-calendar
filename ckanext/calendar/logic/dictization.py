import ckan.model as m


def event_dictize(obj):
    out = obj.as_dict()

    creator = m.User.get(out['creator_id'])
    out['creator'] = creator.name
    del out['creator_id']
    return out
