from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from campmanager.models import Burner, Group, Area, SubCamp, CACHE_KEY
from django.core.cache import cache

def group(request, siteid):

    saved = request.GET.get('saved', '')
    setup = request.GET.get('setup', '')
    msg = None
    groups = Group.objects.filter(id=siteid)
    if groups:
        group = groups[0]
    else:
        group = Group()
        group.user = request.user
        group.numpeople = 0

    if request.method == 'POST':
        group.numpeople = 0
        group.user = request.user
        group.name = request.POST['name'] 
        group.desc = request.POST['desc'] 
        group.type = request.POST['type'] 
        print group.type
    
        subcamps = SubCamp.objects.filter(name=request.POST['subcamp'])
        if subcamps:
            group.subcamp = subcamps[0]
        else:
            msg = "Error: Somehow you managed to pick an non existing camp."
            
        try:
            group.numpeople = int(request.POST['numpeople'])
            if group.numpeople <= 0: raise ValueError
        except ValueError:
            msg = "Error: Please enter a positive number for number of people!"
            group.numpeople = 0

        if int(siteid) == 0:
            try:
                check = Group.objects.get(name__iexact=group.name)
                msg = "Error: That site already exists. Please pick a different name."
            except Group.DoesNotExist:
                pass

        if not msg:
            if group.name == "" or group.desc == "": msg = "Error: Please enter the name of the group and a short description."
            if not msg:
                cache.delete(CACHE_KEY)
                group.save()
                return HttpResponseRedirect('/group/%s/?saved=1' % group.id)

    if saved:
        msg = "Group registration saved. Thanks for registering!"

    subcamps = SubCamp.objects.all().order_by('name')
    areas = Area.objects.filter(group=siteid).order_by('-name')
    if int(siteid) == 0:
        title = "Register new group"
    else:
        title = "Group: %s" % group.name
    t = loader.get_template('campmanager/group/group')
    c = RequestContext(request, {
        'msg' : msg,
        'group': group,
        'areas': areas,
        'owner' : request.user.username == group.user.username,
        'subcamps' : subcamps,
        'setup' : setup,
        'title' : title,
    })
    return HttpResponse(t.render(c))
