from __future__ import unicode_literals
import hashlib
import os.path
import urllib
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User)
    # location = models.CharField(max_length=50, null=True, blank=True)
    # url = models.CharField(max_length=50, null=True, blank=True)
    # job_title = models.CharField(max_length=50, null=True, blank=True)
    user_sex = (('MALE', 'Male'), ('FEMALE', 'Female'))
    sex = models.CharField(max_length=6, default='Male', choices=user_sex)
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    phone = PhoneNumberField(blank=True)
    zip = models.IntegerField(null=True, blank=True)
    about = models.CharField(max_length=250, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    account_type = models.IntegerField(default=-1)

    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username

    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + \
                       self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' + \
                          self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                )
                return gravatar_url

        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    # def notify_liked(self, feed):
    #     if self.user != feed.user:
    #         Notification(notification_type=Notification.LIKED,
    #                      from_user=self.user, to_user=feed.user,
    #                      feed=feed).save()

    # def unotify_liked(self, feed):
    #     if self.user != feed.user:
    #         Notification.objects.filter(notification_type=Notification.LIKED,
    #                                     from_user=self.user, to_user=feed.user,
    #                                     feed=feed).delete()
    #
    # def notify_commented(self, feed):
    #     if self.user != feed.user:
    #         Notification(notification_type=Notification.COMMENTED,
    #                      from_user=self.user, to_user=feed.user,
    #                      feed=feed).save()
    #
    # def notify_also_commented(self, feed):
    #     comments = feed.get_comments()
    #     users = []
    #     for comment in comments:
    #         if comment.user != self.user and comment.user != feed.user:
    #             users.append(comment.user.pk)
    #
    #     users = list(set(users))
    #     for user in users:
    #         Notification(notification_type=Notification.ALSO_COMMENTED,
    #                      from_user=self.user,
    #                      to_user=User(id=user), feed=feed).save()


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#
# # post_save.connect(create_user_profile, sender=User)
# # post_save.connect(save_user_profile, sender=User)


class Employee(models.Model):
    user = models.OneToOneField(User)
    manager = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    # profile = models.OneToOneField(Profile)
    # date_of_birth = models.DateField(null=True)
    # sex = models.CharField(max_length=6)
    designation = models.CharField(max_length=6)

    class Meta:
        db_table = 'auth_employee'


class Client(models.Model):
    # profile = models.OneToOneField(Profile)
    user = models.OneToOneField(User)
    # company_name = models.CharField(max_length=150)
    # registration_info = models.CharField(max_length=150)
    # website = models.URLField(max_length=200)
    # additional_info = models.CharField(max_length=200)

    class Meta:
        db_table = 'auth_client'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    if instance.profile.account_type == 0:
        if not Client.objects.filter(user=instance).exists():
            Client.objects.create(user=instance)
            instance.client.save()
        else:
            instance.client.save()

            # try:
            #     client = Client.objects.filter(user=instance)
            #     instance.client.save()
            # except Client.DoesNotExist:
            #     Client.objects.create(user=instance)
            #     instance.client.save()

    if instance.profile.account_type == 1 or instance.profile.account_type == 2 or instance.profile.account_type == 3:
        if not Employee.objects.filter(user=instance).exists():
            Employee.objects.create(user=instance)
            instance.employee.save()
        else:
            instance.employee.save()
