from django.db import models

# Create your models here.
class Login_info(models.Model):
	username = models.EmailField(verbose_name='username', max_length=32)
	email = models.CharField(verbose_name="email", max_length=32)
	phone = models.CharField(verbose_name="phone", max_length=32)
	password = models.CharField(verbose_name="password", max_length=32)

