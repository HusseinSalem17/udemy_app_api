from django.db import models
from django.conf import settings

from authentication.models import CustomUser
from course.models import Course


# In your Order model, add the stripe_session_id field to store the Stripe session ID
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)
    stripe_session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
