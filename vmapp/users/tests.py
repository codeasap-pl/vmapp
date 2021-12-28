from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.validators import ValidationError

from users.models import User
from domains.models import Domain


class TestUsers(TestCase):
    def test_create_invalid(self):
        with self.assertRaises(IntegrityError):
            User.objects.create()

    def test_create_invalid_domain(self):
        domain = Domain(domain="this-is-never-saved")
        with self.assertRaises(ValueError):
            User.objects.create(
                domain=domain,
                username="test-create",
                password="test-create-password",
            )

    def test_username_missing(self):
        domain = Domain.objects.create(domain="username-missing")
        with self.assertRaises(ValidationError):
            user = User(
                domain=domain,
                username="",
                password="test-username-missing-password",
            )
            user.full_clean()

    def test_username_too_long(self):
        domain = Domain.objects.create(domain="username-too-long.localhost")
        with self.assertRaises(ValidationError):
            user = User(
                domain=domain,
                username="a" * 128,
                password="test-username-too-long-password",
            )
            user.full_clean()

    def test_create_valid(self):
        domain = Domain.objects.create(domain="create-valid.localhost")
        user = User(
            domain=domain,
            username="test-create-valid",
            password="test-create-valid-password",
            quota=12345,
            is_enabled=True,
        )
        user.full_clean()
        user.save()
        self.assertTrue(user.id, "saved")

    def test_quota(self):
        domain = Domain.objects.create(domain="test-quota.localhost")
        user = User(
            domain=domain,
            username="test-quota",
            password="test-quota-password",
        )

        user.quota = -10
        with self.assertRaises(ValidationError):
            user.full_clean()

        user.quota = "abcd"
        with self.assertRaises(ValidationError):
            user.full_clean()

        user.quota = 100
        user.save()
        self.assertEqual(user.quota, 100 * 1024 * 1024, "Quota in bytes")

    def test_from_db(self):
        domain = Domain.objects.create(domain="test-from-db.localhost")
        user = User.objects.create(
            domain=domain,
            username="test-from-db",
            password="test-from-db-password",
            quota=100,
        )

        self.assertEqual(user.quota, 100 * 1024 * 1024, "Quota in bytes")

        user = User.objects.get(pk=user.id)
        self.assertEqual(user.quota, 100, "Quota in megabytes")

    def test_is_enabled(self):
        domain = Domain.objects.create(domain="test-is-enabled.localhost")
        user = User.objects.create(
            domain=domain,
            username="test-is-enabled",
            password="test-is-enabled-password",
            quota=123456,
        )

        self.assertTrue(user.is_enabled, "Default: is_enabled")

        user.is_enabled = False
        user.save()
        user.refresh_from_db()

        self.assertFalse(user.is_enabled, "Default: is_enabled")

    def test_password_validation(self):
        domain = Domain.objects.create(domain="test-password.localhost")
        # too short
        with self.assertRaises(ValidationError):
            user = User(
                domain=domain,
                username="test-password-validation",
                password="a" * 7,
            )
            user.full_clean()

        # too long
        with self.assertRaises(ValidationError):
            user = User(
                domain=domain,
                username="test-password-validation",
                password="a" * 257,
            )
            user.full_clean()

    def test_password(self):
        password = "test-password-password"
        domain = Domain.objects.create(domain="test-password.localhost")
        user = User.objects.create(
            domain=domain,
            username="test-password",
            password=password,
            quota=123456,
        )

        user.refresh_from_db()

        self.assertNotIn(user.password, password, "Hashed")
        self.assertTrue(
            user.password.startswith("{SHA512-CRYPT}$6$"),
            "Crypted, salted, SHA-512"
        )

    def test_hashed_password(self):
        password = "test-hashed-password"
        domain = Domain.objects.create(domain="test-hashed-password.localhost")
        user = User.objects.create(
            domain=domain,
            username="test-hashed-password",
            password=password,
            quota=123456,
        )

        user.refresh_from_db()

        self.assertNotIn(user.password, password, "Hashed")
        hashed = user.password
        self.assertTrue(
            hashed.startswith("{SHA512-CRYPT}$6$"),
            "Crypted, salted, SHA-512"
        )
        self.assertNotIn(user.password, password, "Hashed")
        # UPDATE RECORD, password should not be changed.
        user.quota = 123
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.password, hashed, "Hashed passw does not change")

        # Change password.
        new_password = password + password
        user.password = new_password
        user.save()
        user.refresh_from_db()
        self.assertNotEqual(user.password, hashed, "Hashed changed OK")
        self.assertNotIn(user.password, new_password, "Updated and hashed")
        self.assertTrue(
            user.password.startswith("{SHA512-CRYPT}$6$"),
            "Crypted, salted, SHA-512"
        )

    def test_str(self):
        domain = Domain.objects.create(domain="test-str.localhost")
        user = User.objects.create(
            domain=domain,
            username="test-str",
            password="test-str-password",
        )

        expected = "test-str@test-str.localhost"
        self.assertEqual(user.email(), expected, "email()")
        self.assertEqual(str(user), expected, "__str__()")
        self.assertEqual(str(user), user.email(), "__str__() calls email()")

    def test_unique_violation(self):
        domain = Domain.objects.create(domain="test-unique.localhost")
        values = dict(
            domain=domain,
            username="test-unique",
            password="test-unique-password",
        )
        User.objects.create(**values)
        with self.assertRaises(IntegrityError):
            User.objects.create(**values)
