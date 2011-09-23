=====================================
django-userpreferences (django-userpreferences)
=====================================

This `Django <https://www.djangoproject.com/>`_ app has for purpose to integrate easily for other apps to use.
It aims to be easily added into existing projects.

Installation 
============

Depedencies  
~~~~~~~~~~~

django-userpreferences requires `django-picklefield <https://github.com/shrubberysoft/django-picklefield>`_.
When upgrading you need `south <http://south.aeracode.org/>`_.

Installing django-userpreferences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install into your python path using pip or easy_install::

    pip install django-userpreferences
    easy_install django-userpreferences

Add *'preferences'* to your INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        ...
        'preferences',
    )

Add *'(r'^preferences/', include('preferences.urls')'* to your urls:: 

    urlpatterns = patterns( '',
        ....
        (r'^preferences/', include('preferences.urls'),
    )

Don't forget to run ::

    ./manage.py syncdb

to create the table that is going to receive the preferences.

And if you are using south (you need south if you are upgrading)::

   ./manage.py migrate

Using django-userpreferences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a *preferences.py* file to you app *test_app*.::

    test_app/
     -- preferences.py
     -- models.py
     -- views.py

That looks like this::

    PREFERENCES = (
        'mailing_period':(
            #(u'Preference Display', 'value')
            (u'Weekly', 'week'), #first item is the default value
            (u'Monthly', 'month'),
            (u'Daily', 'day'),
        )
    )

You can now access user preference within your views::

    >>> user.preferences['test_app']
    {'mailing_period' : 'week'}

    >>> user.preferences['test_app'] = { 'mailing_period' : 'month' }
    >>> user.preferences.save()
    >>> user.preferences['test_app']
    {'mailing_period' : 'month'}

Note: Though it may have some properties of a dict, `user.preferences` is NOT a dict. It's a Model object, dict behaviour is a shortcut for `user.preferences.preferences`.
If you use the preferences urls, an url is made accessible to change preferences::

    <a href="{% url preferences.views.change 'test_app' 'mailing_period' 'month' %}?return_url='/'>Receive monthly newsletter</a>
        
If the value in the database does not match any of the preferences within your 
preferences.py, the default value will be returned (this allows to disable 
preferences after people actually used them without breaking your app)

String settings work nice, I did not try other things such as datetime yet, 
hopefully they work nice (as the settings are stored in a picklefield).

Only discrete set of settings are allowed for now. Patches welcome for 
preferences that could set by user input.

Changing the default separator 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
djatngo-userpreferences uses a separator between the app name and the
preference name in forms. By default the separator is '/'. To override this
in the weird case you might be needing it in some variable name, you need
to change it in you settings.py file::

    PREFERENCES_SEPARATOR = '/'
