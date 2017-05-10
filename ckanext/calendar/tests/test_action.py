from nose.tools import assert_raises
from datetime import datetime
from datetime import timedelta

from ckan.tests import helpers, factories
from ckan import plugins
from ckan import logic
from ckanext.calendar.model import setup as setup_calendar_db


class ActionBase(object):
    @classmethod
    def setup_class(self):
        if not plugins.plugin_loaded('calendar'):
            plugins.load('calendar')

    def setup(self):
        helpers.reset_db()
        setup_calendar_db()


    @classmethod
    def teardown_class(self):
        if plugins.plugin_loaded('calendar'):
            plugins.unload('calendar')


class TestCalendarActions(ActionBase):


    def test_event_create_valid(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)
        data_dict = {
            'title': 'Test event',
            'venue': 'Shirok Sokak',
            'description': 'Making the world a better place',
            'start': str(start),
            'end': str(end),
        }

        result = helpers.call_action('event_create',
                                     context=context, **data_dict)

        assert result['title'] == data_dict['title']
        assert result['venue'] == data_dict['venue']
        assert result['description'] == data_dict['description']
        assert result['start'] == data_dict['start']
        assert result['end'] == data_dict['end']

    def test_event_create_missing_values(self):
        # 'title', 'start' and 'end' are required values

        user = factories.Sysadmin()
        context = {'user': user['name']}

        assert_raises(logic.ValidationError,
                      helpers.call_action,
                      'event_create',
                      context=context)

    def test_event_create_invalid_values(self):
        # 'start' and 'end' must contain dates in ISO format

        user = factories.Sysadmin()
        context = {'user': user['name']}

        data_dict = {
            'title': 'Test event',
            'start': '2017',
            'end': '2017',
        }

        assert_raises(logic.ValidationError,
                      helpers.call_action,
                      'event_create',
                      context=context,
                      **data_dict)

    def test_event_delete_valid(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)
        data_dict = {
            'title': 'Test event',
            'start': str(start),
            'end': str(end)
        }

        result = helpers.call_action('event_create',
                                     context=context, **data_dict)

        event_id = result['id']

        data_dict = {
            'id': event_id
        }

        result = helpers.call_action('event_delete',
                                     context=context, **data_dict)

        assert result['message'] == 'Event successfully deleted'

    def test_event_delete_event_not_found(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        data_dict = {
            'id': 'invalid_id'
        }

        assert_raises(logic.NotFound,
                      helpers.call_action,
                      'event_delete',
                      context=context,
                      **data_dict)

    def test_event_delete_missing_id(self):
        # 'id' is a required value

        user = factories.Sysadmin()
        context = {'user': user['name']}

        assert_raises(logic.ValidationError,
                      helpers.call_action,
                      'event_delete',
                      context=context)

    def test_event_show_valid(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)
        data_dict_create = {
            'title': 'Test event',
            'start': str(start),
            'end': str(end)
        }

        result = helpers.call_action('event_create',
                                     context=context, **data_dict_create)

        event_id = result['id']

        data_dict_show = {
            'id': event_id
        }

        result = helpers.call_action('event_show',
                                     context=context, **data_dict_show)

        assert result['title'] == data_dict_create['title']
        assert result['start'].split(" ")[0] == data_dict_create['start']
        assert result['end'].split(" ")[0] == data_dict_create['end']

    def test_event_show_missing_id(self):
        # 'id' is a required value

        user = factories.Sysadmin()
        context = {'user': user['name']}

        assert_raises(logic.ValidationError,
                      helpers.call_action,
                      'event_show',
                      context=context)

    def test_event_show_event_not_found(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        data_dict = {
            'id': 'invalid_id'
        }

        assert_raises(logic.NotFound,
                      helpers.call_action,
                      'event_show',
                      context=context,
                      **data_dict)

    def test_event_list_empty(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}

        result = helpers.call_action('event_list',
                                     context=context)

        assert len(result['events']) == 0

    def test_event_list_with_single_event(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)

        data_dict = {
            'title': 'Test event',
            'start': str(start),
            'end': str(end),
        }

        helpers.call_action('event_create',
                            context=context, **data_dict)

        result = helpers.call_action('event_list',
                                     context=context)

        assert len(result['events']) == 1
        events = result['events']
        assert events[0]['title'] == data_dict['title']
        assert events[0]['start'].split(" ")[0] == data_dict['start']
        assert events[0]['end'].split(" ")[0] == data_dict['end']

    def test_event_list_with_ten_events(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)

        data_dict = {
            'title': 'Test event',
            'start': str(start),
            'end': str(end),
        }

        # Create 10 events
        for i in range(10):
            helpers.call_action('event_create',
                                context=context, **data_dict)

        result = helpers.call_action('event_list',
                                     context=context)

        # If 'limit' is not specified, the default is the last 5 created events
        assert len(result['events']) == 5

        result = helpers.call_action('event_list',
                                     context=context, limit=8)

        assert len(result['events']) == 8

    def test_event_patch_valid(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)

        data_dict_create = {
            'title': 'Test event',
            'start': str(start),
            'end': str(end),
        }

        result = helpers.call_action('event_create',
                                     context=context, **data_dict_create)

        event_id = result['id']

        data_dict_patch = {
            'id': event_id,
            'title': 'New event title'
        }

        result = helpers.call_action('event_patch',
                                     context=context, **data_dict_patch)

        assert result['title'] == data_dict_patch['title']
        assert result['start'].split(" ")[0] == data_dict_create['start']
        assert result['end'].split(" ")[0] == data_dict_create['end']

    def test_event_patch_missing_id(self):
        # 'id' is a required value

        user = factories.Sysadmin()
        context = {'user': user['name']}

        assert_raises(logic.ValidationError,
                      helpers.call_action,
                      'event_patch',
                      context=context)

    def test_event_patch_event_not_found(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        data_dict = {
            'id': 'invalid_id'
        }

        assert_raises(logic.NotFound,
                      helpers.call_action,
                      'event_patch',
                      context=context,
                      **data_dict)

    def test_event_update_valid(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)

        data_dict = {
            'title': 'Test event',
            'venue': 'Shirok Sokak',
            'description': 'Making the world a better place',
            'start': str(start),
            'end': str(end),
        }

        result = helpers.call_action('event_create',
                                     context=context, **data_dict)

        event_id = result['id']
        start = start + timedelta(days=1)
        end = end + timedelta(days=1)

        data_dict = {
            'id': event_id,
            'title': 'Updated event title',
            'start': str(start),
            'end': str(end),
        }

        result = helpers.call_action('event_update',
                                     context=context, **data_dict)

        assert result['title'] == data_dict['title']
        assert result['start'].split(" ")[0] == data_dict['start']
        assert result['end'].split(" ")[0] == data_dict['end']

    def test_event_update_missing_values(self):
        # 'id' , 'title', 'start' and 'end' are required values

        user = factories.Sysadmin()
        context = {'user': user['name']}

        assert_raises(logic.ValidationError,
                      helpers.call_action,
                      'event_update',
                      context=context)

    def test_event_update_invalid_values(self):
        # 'start' and 'end' must contain dates in ISO format

        user = factories.Sysadmin()
        context = {'user': user['name']}
        start = datetime.utcnow().date()
        end = datetime.utcnow().date() + timedelta(days=1)

        data_dict = {
            'title': 'Test event',
            'venue': 'Shirok Sokak',
            'description': 'Making the world a better place',
            'start': str(start),
            'end': str(end),
        }

        result = helpers.call_action('event_create',
                                     context=context, **data_dict)

        event_id = result['id']

        data_dict = {
            'id': event_id,
            'title': 'Test event',
            'start': '2017',
            'end': '2017',
        }

        assert_raises(logic.ValidationError,
                      helpers.call_action,
                      'event_update',
                      context=context,
                      **data_dict)
