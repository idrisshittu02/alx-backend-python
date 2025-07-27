from rest_framework import permissions
from .models import Conversation

class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        if hasattr(obj 'participants'):
            return request.user in obj.participants.all()
        return False

class IsParticipantOfConversation(permission.BasePermission):
    """Custom permission to check if the user is a participant of the conversation."""
    
    def has_object_permission(self, request, view):
        # Check if is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Handle for Message objects linked to Conversation
    if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        return request.user in obj.conversation.participants.all()
        # Handle for Conversation objects
    elif hasattr(obj, 'participants'):
        return request.user in obj.participants.all()
    return False