from django.test import TestCase
from django.utils import timezone
from authorization.models import CustomUser


class CustomUserTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='jondoe@gmail.com',
            first_name='Jon',
            last_name='Doe',
            phone_number='+2348100909039',
            date_joined=timezone.now()
        )
        self.user2 = CustomUser.objects.create(
            email='test332@example.com',
            first_name='Test',
            last_name='User2',
            phone_number='0987654321'
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(self.user.email, 'jondoe@gmail.com')
        self.assertEqual(self.user.get_full_name(), 'Jon Doe')
        self.assertEqual(self.user.phone_number, '+2348100909039')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_username_field(self):
        self.assertEqual(CustomUser.USERNAME_FIELD, 'email')

    def test_required_fields(self):
        self.assertListEqual(CustomUser.REQUIRED_FIELDS, [
                             'first_name', 'last_name', 'phone_number'])
