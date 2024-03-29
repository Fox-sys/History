# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import AbstractUser
from random import choice
from string import ascii_letters

class MainUser(AbstractUser):
    """
    Main user model in project.
    Used for authentification.
    """
    middle_name = models.CharField(max_length=150, blank=True)
    email_is_hidden = models.BooleanField(default=True)
    phone = models.CharField(max_length=12, blank=True)
    phone_is_hidden = models.BooleanField(default=True)
    avatar = models.FileField(upload_to="user_avatars/", default="user_avatars/default.png")
    uploads = models.ManyToManyField("SolderPost", blank=True)
    uploads_amount = models.PositiveIntegerField(default=0)
    is_moderator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=20, default=''.join(choice(ascii_letters) for i in range(20)))

    def __str__(self):
        return f"{self.id} - {self.username} {self.last_name} {self.first_name} {self.uploads_amount}"

    def get_absolute_url(self):
        return f'/profiles/{self.id}'


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class SolderPost(models.Model):
    """
    Model for representation post with Solders
    """
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    desc = models.TextField()
    birth_date = models.DateField()
    death_date = models.DateField(blank=True, null=True)
    is_alive = models.BooleanField(default=False)
    photo = models.FileField(upload_to="solder_photos/")
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return f"{self.id} - {self.last_name} {self.first_name} {self.is_alive}"

    def get_absolute_url(self):
        return f'/solders/{self.id}'


    class Meta:
        verbose_name = "Солдат"
        verbose_name_plural = "Солдаты"



class Exhibit(models.Model):
    """
    Model for representation museum exhibits
    """
    name = models.CharField(max_length=150)
    desc = models.TextField()
    image = models.FileField(upload_to="museum_photos")

    def __str__(self):
        return f"{self.id} - {self.name}"

    def get_absolute_url(self):
        return f'/exhibits/{self.id}'


    class Meta:
        verbose_name = "Экспонат"
        verbose_name_plural = "Экспонаты"
    

class BadWord(models.Model):
    """
        Words that shouldn't be on the site
    """
    word = models.CharField("Слово", max_length=150)
    
    def __str__(self):
        # return f'{self.word}'.encode('windows-1251').decode('utf-8') # if using windows
        return f'{self.word}'

    class Meta:
        verbose_name = "Плохое слово"
        verbose_name_plural = "Плохие слова"

    def __unicode__(self):
        return self.word


class Tag(models.Model):
    tag = models.CharField('Тэг', max_length=100)

    def __str__(self):
        return f'{self.tag}'

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
