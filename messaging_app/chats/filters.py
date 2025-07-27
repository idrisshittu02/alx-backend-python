import django_filters
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    conversation = django_filters.CharFilter(field_name='conversation__id', lookup_expr='exact')
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']