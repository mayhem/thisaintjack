from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from campmanager.models import Burner, CampSite, Area, SubCamp, CACHE_KEY
from django.core.cache import cache

def campsite(request, siteid):

    msg = None
    campsites = CampSite.objects.filter(id=siteid)
    if campsites:
        campsite = campsites[0]
    else:
        campsite = CampSite()
        campsite.user = request.user
        campsite.numpeople = 0

    if request.method == 'POST':
        campsite.numpeople = 0
        campsite.user = request.user
        campsite.name = request.POST['name'] 
        campsite.desc = request.POST['desc'] 
    
        subcamps = SubCamp.objects.filter(name=request.POST['subcamp'])
        if subcamps:
            campsite.subcamp = subcamps[0]
        else:
            msg = "Error: Somehow you managed to pick an non existing subcamp, you tard."
            
        try:
            campsite.numpeople = int(request.POST['numpeople'])
            if campsite.numpeople <= 0: raise ValueError
        except ValueError:
            msg = "Error: Please enter a positive number for number of people, you numbskull!"
            campsite.numpeople = 0

        if int(siteid) == 0:
            try:
                check = CampSite.objects.get(name__iexact=campsite.name)
                msg = "Error: That site already exists. Please pick a different name, you wanker."
            except CampSite.DoesNotExist:
                pass

        if not msg:
            if campsite.name == "" or campsite.desc == "": msg = "Error: Please enter the name of the camp site and a short description."
            if not msg:
                cache.delete(CACHE_KEY)
                campsite.save()
                msg = "Site saved"

    subcamps = SubCamp.objects.all().order_by('name')
    areas = Area.objects.filter(campsite=siteid).order_by('-name')
    t = loader.get_template('campmanager/campsite/site')
    c = RequestContext(request, {
        'msg' : msg,
        'campsite': campsite,
        'areas': areas,
        'owner' : request.user.username == campsite.user.username,
        'subcamps' : subcamps
    })
    return HttpResponse(t.render(c))
