from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*\d+)(?=.*[A-Z])[0-9a-zA-Z!@#$%]{8,255}$')


class Manager(models.Manager):
    def validator(self, postData):
        x = {}

        if len(postData['first_name']) == 0 :
            x['first_name']= "First name must not be empty"
        if len(postData['first_name']) > 255 :
            x['first_name']= "Course name can not be more than 255 characters"

        if len(postData['last_name']) == 0 :
            x['last_name']= "Last name must not be empty"
        if len(postData['last_name']) > 255 :
            x['last_name']= "Last name can not be more than 255 characters"
        
        if len(postData['email']) == 0 :
            x['email']= "Email must not be empty"
        if len(postData['email']) > 255 :
            x['email']= "Email can not be more than 255 characters"

        if len(postData['password']) < 8 :
            x['password']= "Password must be at least 8 characters"
        if len(postData['password']) > 255 :
            x['password']= "Password can not be more than 255 characters"
        elif  not postData['password'] == postData['confirmpassword']:
            x['password']= "Password does not match with the confirmation"
        elif not PW_REGEX.match(postData['password']):             
            x['password']= "Need at least one number and one capital letter for the password"
            
        return x
    
    def infovalidator(self, postData):
        x = {}
        if len(postData['first_name']) == 0 :
            x['first_name']= "First name must not be empty"
        if len(postData['first_name']) > 255 :
            x['first_name']= "Course name can not be more than 255 characters"

        if len(postData['last_name']) == 0 :
            x['last_name']= "Last name must not be empty"
        if len(postData['last_name']) > 255 :
            x['last_name']= "Last name can not be more than 255 characters"
        
        if len(postData['email']) == 0 :
            x['email']= "Email must not be empty"
        if len(postData['email']) > 255 :
            x['email']= "Email can not be more than 255 characters"

        return x
    
    def passvalidator(self, postData):
        x = {}
        if len(postData['password']) < 8 :
            x['password']= "Password must be at least 8 characters"
        if len(postData['password']) > 255 :
            x['password']= "Password can not be more than 255 characters"
        elif  not postData['password'] == postData['confirmpassword']:
            x['password']= "Password does not match with the confirmation"
        elif not PW_REGEX.match(postData['password']):             
            x['password']= "Need at least one number and one capital letter for the password"
            
        return x





class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    user_level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = Manager()

    # def __repr__(self):
    #     return "{} {}".format(self.first_name, self.last_name)

class Message(models.Model):
    messagecontext = models.TextField()
    author = models.ForeignKey(User, related_name="sentmessages")
    receiver = models.ForeignKey(User, related_name="receivedmessages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    commentcontext = models.TextField()
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)