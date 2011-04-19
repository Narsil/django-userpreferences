from utils import render_to_response
from models import PREFERENCES
from django.contrib.auth.decorators import login_required
import os
import django.views.static
import app_settings
from django.http import Http404

@login_required
def index(request):
    if request.method=="POST":
        post = request.POST
        for key,value in post.items():
            toks = key.split(app_settings.SEPARATOR)
            if len(toks)!=2:
                continue
            app,pref = toks[0],toks[1]
            # User choice is always in first place [0].
            # Value of preference is always in second place [1]
            preferences=request.user.preferences.all()
            if preferences[app][pref][0][1] != value:
                user_preferences = request.user.preferences.preferences
                app_pref = user_preferences.get(app)
                if not user_preferences.has_key(app):
                    user_preferences[app]={}
                if not user_preferences[app].has_key(pref):
                    user_preferences[app][pref]={}
                user_preferences[app][pref]=value
                request.user.preferences.save()
    preferences=request.user.preferences.all()
    extra={
            'preferences':preferences ,
            "SEPARATOR": app_settings.SEPARATOR}
    return render_to_response('preferences.html',request,extra=extra)

def media(request, path):
    parent = os.path.abspath(os.path.dirname(__file__))
    root = os.path.join(parent, 'media')
    return django.views.static.serve(request, path, root)
