from django.db import models
from django.contrib.auth import models as auth_models
from picklefield.fields import PickledObjectField
import fields

from django.conf import settings
PREFERENCES={}
for app in settings.INSTALLED_APPS:
    try:
        _temp = __import__(app,globals(),locals(),['preferences'],-1)
        prefs = _temp.preferences.PREFERENCES
        PREFERENCES.update({app:prefs})
    except:
        pass

class UserPreferences(models.Model):
    user = fields.AutoOneToOneField(
            auth_models.User,
            related_name='preferences',
            null=True)
    preferences = PickledObjectField(default={})

    def get(self,app_label):
        app_prefs = PREFERENCES.get(app_label)
        prefs={}
        for key in app_prefs:
            #0 because it's the default choice
            #1 because we want to take the key not the value
            prefs[key]=app_prefs[key][0][1]
        if not prefs:
            return {}
        user_prefs = self.preferences.get(app_label)
        if user_prefs:
            for key in user_prefs:
                #1 because we want to take the key not the value
                prefs[key]=user_prefs[key]
        return prefs

    def all(self):
        #reorders preferences to put current user preferences as first item
        preferences = PREFERENCES
        for app_label in PREFERENCES:
            user_prefs = self.preferences.get(app_label)
            if not user_prefs:
                continue
            for pref,user_value in user_prefs.items():
                possibilities = list(preferences[app_label][pref])
                for index,item in enumerate(possibilities):
                    if item[1] == user_value:
                        user_item = possibilities.pop(index)
                        possibilities.insert(0,user_item)
                        break
                preferences[app_label][pref]=tuple(possibilities)
        return preferences




