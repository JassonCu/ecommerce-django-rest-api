from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from cart.models import Cart
from user_profile.models import UserProfile
from wishlist.models import WishList
from django.utils.translation import gettext_lazy as _

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        shopping_cart = Cart.objects.create(user=user)
        shopping_cart.save()
        
        profile = UserProfile.objects.create(user=user)
        profile.save()
        
        wishlist = WishList.objects.create(user=user)
        wishlist.save()

        return user

    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('Email'))
    first_name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    last_name = models.CharField(max_length=255, verbose_name=_('Apellido'))
    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff'))

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email