import time
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth

class AutoLogout:
    def process_request(self, request):
        if not request.user.is_authenticated():
            #Can't log out if not logged in
            return
        try:
            max_age = settings.SESSION_COOKIE_AGE
            last_touch = request.session['last_touch']
            #time_last = time.localtime(int(last_touch))
            if datetime.now() - last_touch > timedelta( 0, max_age, 0):
                print 'Success auto logout: %s' % (last_touch)
                auth.logout(request)
                del request.session['last_touch']
                return
        except Exception, e:
            request.session['last_touch'] = datetime.now()
            pass
        else:
            request.session['last_touch'] = datetime.now()
