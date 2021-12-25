from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.validators import ValidationError

from aliases.models import Alias


class TestAliases(TestCase):
    def test_create_invalid(self):
        with self.assertRaises(ValidationError):
            Alias().full_clean()

    def test_create_missing_email(self):
        with self.assertRaises(ValidationError):
            Alias(alias="missing-email@localhost").full_clean()

    def test_create_missing_alias(self):
        with self.assertRaises(ValidationError):
            Alias(email="missing-alias@localhost").full_clean()

    def test_unique_violation(self):
        email = "unique@localhost"
        alias = "unique-alias@localhost"
        o = Alias.objects.create(email=email, alias=alias)
        self.assertTrue(o.id)
        with self.assertRaises(IntegrityError):
            Alias.objects.create(email=email, alias=alias)

    def test_lengths(self):
        with self.assertRaises(ValidationError):
            Alias(
                email="aa",
                alias="length-1-alias@localhost",
            ).full_clean()

        with self.assertRaises(ValidationError):
            Alias(
                email="length-2@localhost",
                alias="aa",
            ).full_clean()

        with self.assertRaises(ValidationError):
            Alias(
                email="a" * 256,
                alias="length-3-alias@localhost",
            ).full_clean()

        with self.assertRaises(ValidationError):
            Alias(
                email="length-3@localhost",
                alias="a" * 256,
            ).full_clean()

    def test_is_enabled(self):
        o = Alias(email="enabled@localhost", alias="enabled-alias@localhost")
        self.assertTrue(o.is_enabled)
        o.is_enabled = False
        o.save()
        o.refresh_from_db()
        self.assertFalse(o.is_enabled)
