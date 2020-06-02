from django.db import models
from log_reg_app.models import User

# Create your models here.
class WishManager(models.Manager):
    def validatorWish(self, postData):
        # Dictionary for saving the message errors
        errors = {}
        
        # Validator for first and last name
        # Validator for first and last name
        if len(postData['item']) < 3:
            errors['item'] = "Your wish item name must be at leat 3 characters."
        if len(postData['description']) < 3:
            errors['description'] = "Your wish description must be at leat 3 characters."
        
        return errors

class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.TextField()
    granted = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User,related_name='wishes_uploaded', on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User,related_name="liked_wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()