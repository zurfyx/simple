from datetime import timedelta
from django.test import TestCase

from users import constants
from users.models import User


class TestDefaultUser(TestCase):

    INACTIVE_AFTER = constants.ACTIVE_DAYS  # days

    def setUp(self):
        super(TestDefaultUser, self).setUp()
        self.user = User(
            email='default@example.com',
        )
        self.user.set_password('password')
        self.user.save()

    def test_is_active_after_creation(self):
        self.assertTrue(self.user.is_active)

    def test_is_active_after_30_days_creation(self):
        self.user.date_joined = self.user.date_joined + \
                                timedelta(days=-self.INACTIVE_AFTER)
        self.user.save()
        self.assertTrue(self.user.is_active)

    def test_is_active_after_30_days_login(self):
        # last login is still null (never logged in) -> we pick date_joined
        self.user.last_login = self.user.date_joined + \
                                timedelta(days=-self.INACTIVE_AFTER)
        self.user.save()
        self.assertTrue(self.user.is_active)

    def test_is_active_after_31_days_creation_30_days_login(self):
        self.user.date_joined = self.user.date_joined + \
                                timedelta(days=-self.INACTIVE_AFTER+1)
        # last login is still null (never logged in) -> we pick date_joined
        self.user.last_login = self.user.date_joined + \
                               timedelta(days=-self.INACTIVE_AFTER)
        self.user.save()
        self.assertTrue(self.user.is_active)

    def test_is_not_active_after_31_days_creation(self):
        self.user.date_joined = self.user.date_joined + \
                                timedelta(days=-self.INACTIVE_AFTER-1)
        self.user.last_login = None
        self.user.save()
        self.assertFalse(self.user.is_active)

    def test_is_not_active_after_31_days_creation_31_days_login(self):
        self.user.date_joined = self.user.date_joined + \
                                timedelta(days=-self.INACTIVE_AFTER-1)
        # last login is still null (never logged in) -> we pick date_joined
        self.user.last_login = self.user.date_joined + \
                               timedelta(days=-self.INACTIVE_AFTER-1)
        self.user.save()
        self.assertFalse(self.user.is_active)

    def test_is_not_superuser(self):
        self.assertFalse(self.user.is_superuser)

    def test_is_not_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_short_name_is_first_name(self):
        pass

    def test_full_name_is_first_name_and_last_name(self):
        pass

    def test_age_is_none_if_null_or_blank(self):
        pass

    def test_age_is_20_if_birthday_was_20_years_ago(self):
        pass


class TestAdminUser(TestCase):

    def setUp(self):
        super(TestAdminUser, self).setUp()
        self.user = User(
            email='admin@example.com',
            is_staff=True,
        )
        self.user.set_password('password')
        self.user.save()

    def test_is_superuser(self):
        self.assertTrue(self.user.is_superuser)

    def test_is_staff(self):
        self.assertTrue(self.user.is_staff)


class TestRoleHeadOfDepartmentUser(TestCase):

    def test_role_str_return_head_of_department(self):
        pass


class TestRoleModeratorUser(TestCase):

    def test_role_str_return_moderator(self):
        pass
