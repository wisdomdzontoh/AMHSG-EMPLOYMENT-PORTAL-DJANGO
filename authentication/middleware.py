# middleware.py

import datetime
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        
        # Get the session timeout period (in seconds)
        timeout = getattr(settings, 'AUTO_LOGOUT_DELAY', 900)  # 900 seconds = 15 minutes
        
        last_activity = request.session.get('last_activity')
        if last_activity:
            now = datetime.datetime.now()
            elapsed_time = (now - datetime.datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S")).total_seconds()

            if elapsed_time > timeout:
                logout(request)
                return  # User has been logged out; stop further processing.

        # Update the last activity time
        request.session['last_activity'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
