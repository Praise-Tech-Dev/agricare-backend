from django.urls import path
from .views import WhatsAppWebhookView

urlpatterns = [
    # The endpoint twilio will call 
    path('whatsapp/webhook/', WhatsAppWebhookView.as_view(), name='whatsapp_webhook')
]