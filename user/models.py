from django.db import models

class Society(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    email_id = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    referal_code = models.CharField(max_length=15,null=True,blank=True)
    wallet_amount = models.FloatField(default=0.0)
    society = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username