from django.db import models
from django.contrib.auth.models import User
from marketplace.models import VendorProfile, CoachProfile, JobPost

class Thread(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='threads')
    coach = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, related_name='threads')
    job_post = models.ForeignKey(JobPost, on_delete=models.SET_NULL, null=True, blank=True, related_name='threads')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['vendor', 'coach']

    def __str__(self):
        return f"Thread: {self.vendor.organization_name} ↔ {self.coach.display_name}"

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()

    @property
    def unread_count_for_vendor(self):
        return self.messages.filter(sender_type='coach', read_by_vendor=False).count()

    @property
    def unread_count_for_coach(self):
        return self.messages.filter(sender_type='vendor', read_by_coach=False).count()

class Message(models.Model):
    SENDER_CHOICES = [
        ('vendor', 'Vendor'),
        ('coach', 'Coach'),
    ]
    
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    body = models.TextField()
    
    # Contact info sharing
    contact_info_shared = models.BooleanField(default=False, help_text="Coach has shared contact info with this vendor")
    
    # Read receipts
    read_by_vendor = models.BooleanField(default=False)
    read_by_coach = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_type}: {self.body[:50]}..."

    def mark_as_read_by_vendor(self):
        if self.sender_type == 'coach':
            self.read_by_vendor = True
            self.save()

    def mark_as_read_by_coach(self):
        if self.sender_type == 'vendor':
            self.read_by_coach = True
            self.save()
