from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_feilds):
        if not phone_number:
            raise ValueError("Phone number is required")
        
        extra_feilds['emails'] = self.normalize_email(extra_feilds['emails'])
        user = self.model(phone_number=phone_number, **extra_feilds)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_feilds):
        extra_feilds.setdefault('is_staff', True)
        extra_feilds.setdefault('is_superuser', True)
        extra_feilds.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_feilds)