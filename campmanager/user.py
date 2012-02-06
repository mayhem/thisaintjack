from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms as forms
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.core.cache import cache
from campmanager.models import Burner, CACHE_KEY

def login(request):
    return render_to_response("campmanager/user/login")

def login_created(request):
    return render_to_response("campmanager/user/login_created")

def login_error(request):
    return render_to_response("campmanager/user/login_error")

def disconnected(request):
    logout(request)
    return HttpResponseRedirect("/")

def newlogin(request):
    form = UserCreationForm()
    if request.method == 'POST':
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            if data['magicword'] == "bacon":
		new_user = form.save(data)
		burner = Burner()
		burner.user = new_user
		burner.save()
		cache.delete(CACHE_KEY)
		user = authenticate(username=data['username'], password=data['password1'])
		if user: login(request, user)
		return HttpResponseRedirect("/user/profile")
            else:
                # this is a total cheat, but doing this without an entry in the model is a pita
                data['badmagicword'] = "1"

    else:
        data, errors = {}, {}
        try:
            del data['badmagicword']
        except KeyError:
            pass

    return render_to_response("campmanager/user/newlogin", {
        'form' : forms.FormWrapper(form, data, errors)
    })

def logoff(request):
    logout(request)
    return HttpResponseRedirect("/")

def myprofile(request):

    msg = None
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login/?next=%s' % request.path)

    burnerList = Burner.objects.filter(user=request.user.id)
    if burnerList: 
        burner = burnerList[0]
    else:
        burner = Burner(user=request.user)

    if request.method == 'POST':
        burner.realname = request.POST['realname'] 
        burner.mobile = request.POST['phone']
        msg = "Profile saved. Click on Register Campsite in the menu bar to register a camp site!"
        burner.save()

    t = loader.get_template('campmanager/user/myprofile')
    c = RequestContext(request, {
            'msg' : msg,
            'realname' : burner.realname,
            'email' : burner.email,
            'phone' : burner.mobile,
    })
    return HttpResponse(t.render(c))

def profile(request, username):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login/?next=%s' % request.path)

    u = User.objects.get(username__exact=username)
    if u:
        burnerList = Burner.objects.filter(user=u.id)
        if burnerList: 
            burner = burnerList[0]
        else:
            burner = Burner()

    t = loader.get_template('campmanager/user/profile')
    if burner:
        c = RequestContext(request, {
                'burner' : username,
                'realname' : burner.realname,
                'email' : burner.email,
                'phone' : burner.mobile,
        })
    else:
        c = RequestContext(request, { 
                'burner' : username,
                'error' : "No such burner, doofus!" });
    return HttpResponse(t.render(c))

def help(request):
    t = loader.get_template('campmanager/user/help')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

