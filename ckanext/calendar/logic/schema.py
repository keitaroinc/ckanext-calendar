from ckan.plugins import toolkit


not_empty = toolkit.get_validator('not_empty')
ignore_missing = toolkit.get_validator('ignore_missing')
not_missing = toolkit.get_validator('not_missing')
isodate = toolkit.get_validator('isodate')
boolean_validator = toolkit.get_validator('boolean_validator')


def event_create_schema():
    return {
        'title': [not_empty, unicode],
        'description': [ignore_missing, unicode],
        'venue': [ignore_missing, unicode],
        'start': [not_empty, isodate],
        'end': [not_empty, isodate],
        'meta': [ignore_missing, unicode],
        'active': [ignore_missing, boolean_validator]
    }


def event_update_schema():
    schema = event_create_schema()
    schema['id'] = [not_empty, unicode]

    return schema


def event_patch_schema():
    return event_update_schema()
