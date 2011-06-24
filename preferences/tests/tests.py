"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from preferences import models
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse

class PreferencesTest(TestCase):
    def setUp(self):
        self.OLD_PREFERENCES = models.PREFERENCES
        self.u = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        models.PREFERENCES={
                'test_app': {
                    'pref_test':(
                        ('default','default_value'),
                        ('different','different_value')),
                    'pref_test2':(
                        ('default2','default_value2'),
                        ('different2','different_value2')),
                    }
                }
        self.u.preferences.preferences['test_app']={
                'pref_test':'default_value',
                'pref_test2':'default_value2',
                }

    def tearDown(self):
        models.PREFERENCES= self.OLD_PREFERENCES

class PreferencesAPITest(PreferencesTest):
    def test_get_default_if_none(self):
        self.u.preferences.preferences['test_app']={}
        self.u.preferences.save()
        test_settings=self.u.preferences.get('test_app')
        self.assertEqual(test_settings,
                {'pref_test':'default_value',
                    'pref_test2':'default_value2'})

    def test_get_default_if_wrong_in_db(self):
        self.u.preferences.preferences['test_app']={'pref_test':'toto'}
        self.u.preferences.save()
        test_settings=self.u.preferences.get('test_app')
        self.assertEqual(test_settings,
                {'pref_test':'default_value',
                    'pref_test2':'default_value2'})


    def test_change_through_api(self):
        self.u.preferences.preferences['test_app']={'pref_test':'different_value'}
        self.u.preferences.save()
        test_settings=self.u.preferences.get('test_app')
        self.assertEqual(test_settings,
                {'pref_test':'different_value',
                    'pref_test2':'default_value2'})


    def test_change_through_dict_api(self):
        self.u.preferences['test_app']={'pref_test':'different_value'}
        self.u.preferences.save()
        test_settings=self.u.preferences['test_app']
        self.assertEqual(test_settings,
                {'pref_test':'different_value',
                    'pref_test2':'default_value2'})

class PreferencesUrlTest(PreferencesTest):
    def test_change_through_url(self):
        url = reverse(
                'preferences.views.change',
                args=['test_app','pref_test','different_value'],
        )
        c = Client()
        c.login(username='testuser',password='testpw')
        response=c.get( url, {'return_url':'/'} )
        self.assertEqual(response.status_code,302)
        test_settings=self.u.preferences.get('test_app')
        self.assertEqual(test_settings,
                {'pref_test':'different_value',
                    'pref_test2':'default_value2'})

    def test_change_through_form(self):
        url = reverse(
                'preferences.views.index',
        )
        c = Client()
        c.login(username='testuser',password='testpw')
        response=c.get( url )
        self.assertEqual(response.status_code,200)
