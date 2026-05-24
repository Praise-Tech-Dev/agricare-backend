from django.db import models
from django.utils import timezone

# profile
class Farmer(models.Model):
    """
    Primary user profile for the platform.
    Identification is based on phone number. 
    """

    phone_number =models.CharField(max_length=20, unique=True, help_text="WhatsApp number with country code")
    name = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=10, default='English', choices=[
        ('English','English'),
        ('Yoruba', 'Yoruba'),
        ('Hausa', 'Hausa'),
    ])

    flock_size = models.IntegerField(default=0, help_text="Number of birds in the poultry form")
    location = models.CharField(max_length=255, null=True, blank=True)
    is_onboarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} ({self.phone_number})"
    
# history 
class Conversation(models.Model):
    """
    Stores every message sent and received via WhatsApp/USSD
    Important for RAG context and audit logs.
    """
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='conservations')
    message_text = models.TextField()
    sender_type = models.CharField(max_length=10, choices=[('Farmer', 'Farmer'), ('AI', 'AI'), ('Vet', 'Vet')])
    timestamp = models.DateTimeField(auto_now_add=True)


class HealthCase(models.Model):
    """
    Created when AI flags a high-risk symptom (HLT escalation).
    Shown on the Vet Dashboard.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('In Progress', 'Vet Responding'),
        ('Resolved', 'Resolved'),
    ]

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    symptoms_summary = models.TextField()
    ai_preliminary_diagnosis = models.TextField(null=True, blank=True)
    severity_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_vet_id = models.IntegerField(null=True, blank=True) # Would link to Django User ID later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Case {self.id} - {self.farmer.phone_number} ({self.status})"
