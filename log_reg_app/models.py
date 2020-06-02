from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def validatorSignUp(self, postData):
        # Dictionary for saving the message errors
        errors = {}
        
        # Validator for first and last name
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be at leat 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at leat 2 characters."
        
        # Validator for email
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email']):
            errors['email'] = "Your email must be a valid email."
        
        # Validator for password
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Your password and confirm password must match."
        
        return errors
    
    def validatorSignIn(self, postData):
        # Dictionary for saving the message errors
        errors = {}

        # email exists and password match?
        try:
            loggedUser = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), loggedUser.password.encode()):
                errors['loggedUser'] = "User or password does not exist in our database"
 
        except User.DoesNotExist:
            loggedUser = None
            errors['loggedUser'] = "User or password does not exist in our database"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # liked_wishes = a list of wishes a given user likes
    # wishes_uploaded = a list of wishes uploaded by a given user