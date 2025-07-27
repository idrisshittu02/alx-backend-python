import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from collections import defaultdict

# Configure the logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create a file handler to log to a file
file_handler = logging.FileHandler('requests.log')
file_handler.setLevel(logging.INFO)

# Create a log formatter
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware to log request details including timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user information (if authenticated)
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Get the timestamp and log the request
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - User: {user} - Path: {request.path}"

        # Log the request to the file
        logger.info(log_message)

        # Call the next middleware or view
        response = self.get_response(request)

        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the application based on time.
    Only allows access between 9 AM and 6 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = current_time.replace(hour=9, minute=0, second=0)
        end_time = current_time.replace(hour=18, minute=0, second=0)

        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access is restricted to 9 AM - 6 PM only.")

        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    """
    Middleware to filter out offensive language in request data.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_count = defaultdict(list)

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api'):
            #Get the user's IP address
            ip_address = self.get_client_ip(request)

            # Get the current time
            current_time = now()

            # Check how many messages the user has sent in the last minute
            if len(self.message_count[ip_address]) >= 5:
                return HttpResponseForbidden("You have sent too many messages. Please wait a minute before sending more.")
            
            # Add the current time to the user's message count
            self.message_count[ip_address].append(current_time)

        #Continue processing the request
        response = self.get_response(request)
        # Clean up old messages
        self.message_count[ip_address] = [t for t in self.message_count[ip_address] if (current_time - t).total_seconds() < 60]
        return response
    
    def get_client_ip(self, request):
        """
        Extract the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class RolepermissionMiddleware:
    """
    Middleware to check user roles and permissions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user has the required role
        if request.user.is_authenticated:
            # Check if the user is either admin or moderator
            if request.user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")
            
        else:
            return HttpResponseForbidden("You must be logged in to access this resource.")
        
        #Call the next middleware or view if the user has the required role
        response = self.get_response(request)
        return response