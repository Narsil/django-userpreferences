=====================================
django-userpreferences (django-userpreferences)
=====================================

This Django_ app has for purpose to integrate easily for other apps to use.
It aims to be easily added into existing projects.

Installation 
============

Depedencies  
~~~~~~~~~~~

django-userpreferences requires django-picklefield.
When upgrading you need south.

Installing django-userpreferences
~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        

Changing the default separator 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-userpreferences uses a separator between the app name and the
preference name in forms. By default the separator is '/'. To override this
in the weird case you might be needing it in some variable name, you need
to change it in you settings.py file::

    PREFERENCES_SEPARATOR = '/'
