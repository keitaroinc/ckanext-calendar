from ckan.tests import helpers, factories
from ckan import plugins


class ActionBase(object):
    @classmethod
    def setup_class(self):
        self.app = helpers._get_test_app()
        if not plugins.plugin_loaded('calendar'):
            plugins.load('calendar')

    def setup(self):
        helpers.reset_db()

    @classmethod
    def teardown_class(self):
        if plugins.plugin_loaded('calendar'):
            plugins.unload('calendar')


class TestCalendarActions(ActionBase):
    def test_event_create(self):
        user = factories.Sysadmin()
        context = {'user': user['name']}
        data_dict = {
            'title': 'Test event',
            'venue': 'Shirok Sokak',
            'description': 'Making the world a better place',
            'start': '2017-02-23 17:00:00',
            'end': '2017-02-23 21:00:00',
        }

        result = helpers.call_action('event_create',
                                     context=context, **data_dict)

        assert result['title'] == data_dict['title']
        assert result['venue'] == data_dict['venue']
        assert result['description'] == data_dict['description']
        assert result['start'] == data_dict['start']
        assert result['end'] == data_dict['end']
