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

burners = Burner.objects.all()
for burner in burners:
    if burner.user.email != 'mayhem@gmail.com': continue

    groups = Group.objects.filter(user=burner.user.id)
    msg =  "Hello %s!\n\n" % burner.realname
    msg += "This email is to remind you that you've signed up to come to the " + \
          "Celebrate Greg party on Oct 13/14.\n\n"
    msg += "You have registered the following group(s):\n\n"

    for group in groups:
        msg += "            name: %s\n" % group.name
        msg += "     description: %s\n" % group.desc
        msg += "number of people: %d\n" % group.numpeople
        msg += " type of camping: %s\n" % types[group.type]
        if group.type != Group.OFFSITE_CAMPING:
            msg += "        sub-camp: %s\n" % group.subcamp.name

        msg += "\n"

    msg += "The most important thing is that the NUMBER OF PEOPLE coming is correct. " + \
          "If the number is NOT correct, please go to http://rsvp.celebrategreg.org TODAY " + \
          "and update this number to the correct number. If you can no longer attend, set this " + \
          "number to ZERO.\n\n"
    msg += "If you have any questions about your group registration, please email aleta.dunne@gmail.com . " + \
          "She will work with you to get your registration squared away.\n\n"
    msg += "Thanks for signing up -- we're looking forward to seeing you next weekend!\n\n"

    print msg
    email("noreply@celebrategreg.org", burner.user.email, "Your Celebrate Greg! group registrations", msg)


