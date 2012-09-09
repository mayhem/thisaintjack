import locale
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.cache import cache
from campmanager.models import Burner, CampSite, Area, SubCamp, CACHE_KEY

def index(request):

    locale.setlocale(locale.LC_ALL, "")
    subcamps = SubCamp.objects.all()

    totalpeople = 0
    totalsqft = 0
    subcamp_list = []
    for subcamp in subcamps:
        subcamppeople = 0
        sites = CampSite.objects.filter(subcamp=subcamp)
        for site in sites:
            totalpeople += site.numpeople
            subcamppeople += site.numpeople

        sqft = int(subcamppeople) * 500
        totalsqft += sqft
        sqft = locale.format("%d", sqft, grouping=True)
        subcamp_list.append({ 'name' : subcamp.name,
                              'numpeople' : subcamppeople,
                              'sqft' : sqft,
                              'desc' : subcamp.desc })

    locale.setlocale(locale.LC_ALL, "")
    totalsqft = locale.format("%d", totalsqft, grouping=True)

    subcamps = SubCamp.objects.all().order_by('-name')
    sites = CampSite.objects.all().order_by('-numpeople')
    t = loader.get_template('campmanager/index')
    c = RequestContext(request, {
        'subcamp_list': subcamp_list,
        'totalpeople' : totalpeople,
        'totalsubcamps' : len(subcamps),
        'totalsqft' : totalsqft
    })
    return HttpResponse(t.render(c))

def subcamp(request, subcamp):

    subcamps = SubCamp.objects.filter(name=subcamp)
    if not subcamps:
        err = "Sub camp %s does not exist, bukkake face!" % subcamp
        t = loader.get_template('campmanager/error')
        c = RequestContext(request, {'err':err})
        return HttpResponse(t.render(c))
    else:
        subcamp = subcamps[0]

    totalpeople = 0
    sites = CampSite.objects.filter(subcamp=subcamp)
    totalsites = len(sites)
    for site in sites:
        totalpeople += site.numpeople

    totalshit = Area.objects.count()

    locale.setlocale(locale.LC_ALL, "")
    totalsqft = locale.format("%d", int(totalpeople) * 500, grouping=True)

    sites = CampSite.objects.filter(subcamp=subcamp).order_by('-numpeople')
    t = loader.get_template('campmanager/subcamp')
    c = RequestContext(request, {
        'subcamp' : subcamp,
        'site_list': sites,
        'totalpeople' : totalpeople,
        'totalsites' : totalsites,
        'totalshit' : totalshit,
        'totalsqft' : totalsqft,
    })
    return HttpResponse(t.render(c))

def burnerlist(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/user/login/?next=%s' % request.path)

    burners = Burner.objects.all().order_by('-realname')
    t = loader.get_template('campmanager/burners')
    c = RequestContext(request, {
        'burners': burners
    })
    return HttpResponse(t.render(c))

def bigshitlist(request):

    bigshit = Area.objects.all().order_by('-name')
    t = loader.get_template('campmanager/bigshit')
    c = RequestContext(request, {
        'bigshits': bigshit
    })
    return HttpResponse(t.render(c))
