from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from campmanager.models import Burner, CampSite, Area, CACHE_KEY
from django.core.cache import cache

def area(request, siteid, shitid):

    msg = None
    campsites = CampSite.objects.filter(id=siteid)
    if campsites:
        campsite = campsites[0]
    else:
        msg = "Cannot load campsite %d" % siteid

    if not msg:
        areas = Area.objects.filter(id=shitid)
        if areas:
            area = areas[0]
        else:
            area = Area()
            area.campsite = campsite
            area.numpeople = 0
            area.width = 0
            area.height = 0

        if request.method == 'POST':
            area.numpeople = 0
            area.user = request.user
            area.name = request.POST['name'] 
            area.desc = request.POST['desc'] 

            if area.name == "" or area.desc == "": msg = "Please enter the name of the big shit and a short description."
            try:
                area.width = int(request.POST['width'])
                area.height = int(request.POST['height'])
                if area.width <= 0 or area.height <= 0: raise ValueError
            except ValueError:
                msg = "Please enter a positive number for both dimensions, tard bucket!"
                area.width = 0
                area.height = 0
            if not msg:
                cache.delete(CACHE_KEY)
                area.save()
                msg = "Big shit saved."

    t = loader.get_template('campmanager/area/area')
    c = RequestContext(request, {
        'msg' : msg,
        'area': area,
        'campsite' : campsite,
        'owner' : request.user.username == campsite.user.username
    })
    return HttpResponse(t.render(c))
