from django.contrib.auth.base_user import BaseUserManager


class EmailUserManager(BaseUserManager):
    """
    User authentication to handle email storage instead of username.
    """

    def _create_user(self, email, password, is_staff, **kwargs):
        """
        Creates new user
        """
        if not email:
            raise ValueError('Enter a valid email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, True, **kwargs)
