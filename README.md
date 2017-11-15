# ckanext-calendar

[![Build Status](https://travis-ci.com/ViderumGlobal/ckanext-calendar.svg?token=spv2MuNH6PW4oxEpxfeY&branch=master)](https://travis-ci.com/ViderumGlobal/ckanext-calendar)

This extension provides an API for using calendar events in CKAN. Standard CRUD
operations can be used.

## Development Installation

To install ckanext-calendar for development, activate your CKAN virtualenv and
do:

```
git clone https://github.com/ViderumGlobal/ckanext-calendar.git
cd ckanext-calendar
python setup.py develop
pip install -r dev-requirements.txt
```

## Config Settings

Add shown events per page limit, default max is 3:

```
ckanext.calendar.events_show_limit = ...
```

Add pagination pages shown limit, default max is 3::

```
ckanext.calendar.pagination_limit = ...
```

Number of events shown in the recent events sidebar, defaults to 5::

```
ckanext.calendar.recent_events_limit = 10
```

The limit for truncating event description, default: 100

```
ckanext.calendar.truncate_limit = ...
```


## API

Available actions to use:

- [event_create](#event_create)
- [event_show](#event_show)
- [event_list](#event_list)
- [event_update](#event_update)
- [event_patch](#event_patch)
- [event_delete](#event_delete)

All above actions can be used both from code with the `get_action()` method, or
through the API.

All actions require sysadmin user, except for `event_show` and `event_list`
which are public and don't require an authenticated user.

> Note: Parameters prefixed with `*` are required.

### `event_create`

The `event_create` action is used to create a single event. It takes the
following input parameters:

Parameter | Type | Description
--------- | ---- | -----------
*title      | string  | Title of an event.
*start      | string  | Start date of an event in ISO format.
*end        | string  | End date of an event in ISO format.
description | string  | Description of an event.
venue       | string  | Venue of an event.
active      | boolean | State of an event. Default is true.
meta        | string  | Additional meta data for an event such as latitude/longitude etc. Data must be sent as an escaped JSON.

Executing the `event_create` action creates additional fields in the database
which are automatically created:

Parameter | Type | Description
--------- | ---- | -----------
id         | string | Unique id of an event.
name       | string | Unique name of an event.
created_at | string | Date of when an event has been created in ISO format.
creator    | string | The user who created an event.

### `event_show`

The `event_show` action is used to retrieve a single event. It takes the
following input parameters:

Parameter | Type | Description
--------- | ---- | -----------
*id | string | Unique id of an event.

### `event_list`

The `event_list` action is used to retrieve a list of last created events. It
takes the following input parameters:

Parameter | Type | Description
--------- | ---- | -----------
limit | int | Number of events to return. Default is 5.

### `event_update`

The `event_update` action is used to update a single event. For all possible
parameters see [event_create](#event_create).

Parameter | Type | Description
--------- | ---- | -----------
*id | string | Unique id of an event.

### `event_patch`

The `event_patch` action is used to patch a single event. The difference
between the update and patch methods is that the patch will perform an update
of the provided parameters, while leaving all other parameters unchanged,
whereas the update method deletes all parameters not explicitly provided. For
all possible parameters see [event_create](#event_create).

Parameter | Type | Description
--------- | ---- | -----------
*id | string | Unique id of an event.

### `event_delete`

The `event_delete` action is used to delete a single event. It takes the
following input parameters:

Parameter | Type | Description
--------- | ---- | -----------
*id | string | Unique id of an event.

## Running the Tests

To run the tests, do:

```
nosetests --ckan --with-pylons=test.ini
```

-------------
Documentation
-------------

In order to view the documentation for all API actions open `documentation/index.html`.

If you want to update or rebuild the documentation please visit the [guide for writing documentation](http://docs.ckan.org/en/latest/contributing/documentation.html).
