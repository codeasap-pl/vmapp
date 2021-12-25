from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.validators import ValidationError

from domains.models import Domain


class TestDomains(TestCase):
    def test_validation(self):
        with self.assertRaises(ValidationError):
            domain = Domain()
            domain.full_clean()
            domain.save()

    def test_validation_domain_length(self):
        with self.assertRaises(ValidationError):
            domain = Domain(domain="")
            domain.full_clean()

    def test_validation_pass(self):
        fqdn = "a"
        domain = Domain(domain=fqdn)
        domain.full_clean()
        domain.save()
        self.assertTrue(domain.id, "saved")
        self.assertEqual(domain.domain, fqdn, "Domain name")

    def test_defaults(self):
        domain = Domain(domain="testing.defaults.localhost")
        domain.full_clean()
        domain.save()
        self.assertTrue(domain.is_enabled, "Default: is_enabled")

    def test_full(self):
        fqdn = "testing.full.is-enabled.localhost"
        domain = Domain(domain=fqdn, is_enabled=False)
        domain.full_clean()
        domain.save()
        self.assertEqual(domain.domain, fqdn, "is_enabled")
        self.assertFalse(domain.is_enabled, "is_enabled")

    def test_unique_violation(self):
        values = dict(
            domain="test-unique-domain.localhost"
        )
        Domain.objects.create(**values)
        with self.assertRaises(IntegrityError):
            Domain.objects.create(**values)

    def test_str(self):
        fqdn = "test-str-domain@localhost"
        domain = Domain.objects.create(domain=fqdn)
        self.assertEqual(str(domain), fqdn, "__str__")
