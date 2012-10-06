#!../../virtualenv/bin/python

import sys, os
import smtplib
from email.mime.text import MIMEText
sys.path.append("../..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thisaintjack.settings")

from campmanager.models import Burner, Group

def email(me, to, subj, txt):

    msg = MIMEText(txt)
    msg['Subject'] = subj
    msg['From'] = me
    msg['To'] = to

    s = smtplib.SMTP('localhost')
    s.sendmail(me, [to], msg.as_string())
    s.quit()

types = {}
for code, desc in Group.CAMP_SITE_TYPE_CHOICES:
    types[code] = desc

print "Sending emails:\n"

burners = Burner.objects.all()
for burner in burners:
    if not burner.user.email:
        print "user %s has no email set. skipping." % burner.realname
        continue

    groups = Group.objects.filter(user=burner.user.id)
    msg =  "Hello %s!\n\n" % burner.realname.encode('utf-8')
    msg += "This email is to remind you that you've signed up to come to the " + \
          "Celebrate Greg party on Oct 13/14.\n\n"
    msg += "You have registered the following group(s):\n\n"

    for group in groups:
        msg += "name: %s\n" % group.name.encode('utf-8')
        msg += "description: %s\n" % group.desc.encode('utf-8')
        msg += "number of people: %d\n" % group.numpeople
        msg += "type of camping: %s\n" % types[group.type].encode('utf-8')
        if group.type != Group.OFFSITE_CAMPING:
            msg += "sub-camp: %s\n" % group.subcamp.name.encode('utf-8')

        msg += "\n"

    msg += "Please verify that the number of people is correct, as well as the type of camping. If these details are " +\
            "NOT correct, please go to http://rsvp.celebrategreg.org TODAY. Log in using the " + \
            "same account you used before, and update the information. If you can no longer attend, set the number " + \
            "of people to ZERO.\n\n"

    msg += "If you have any questions about your group registration, please email aleta.dunne@gmail.com . " + \
           "She will work with you to get your registration squared away.\n\n"
    msg += "Thanks for signing up -- we're looking forward to seeing you next weekend!\n\n"

    print burner.user.email, burner.realname
    #email("noreply@celebrategreg.org", burner.user.email, "Your Celebrate Greg! group registrations", msg)
