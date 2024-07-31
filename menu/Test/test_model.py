from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from menu.models import MenuItemImage, MenuItemTag, MenuItem, Rating, Review
from authorization.models import CustomUser
import uuid


class MenuItemImageTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test2@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            date_joined=timezone.now()
        )
        self.menu_item = MenuItem.objects.create(
            user_id=self.user,
            name='Test Menu Item',
            description='Test Description',
            category='Test Category',
            price=10.00
        )
        image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        self.menu_item_image = MenuItemImage.objects.create(
            menu_item=self.menu_item,
            image=SimpleUploadedFile(
                "test_image.gif", image_content, content_type="image/gif")
        )
        self.menu_item_tag = MenuItemTag.objects.create(name='Test Tag')
        self.rating = Rating.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            rating=4
        )
        self.review = Review.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            rating=self.rating,
            comment='Test Comment'
        )

    def test_menu_item_image_creation(self):
        self.assertTrue(isinstance(self.menu_item_image, MenuItemImage))
        self.assertEqual(self.menu_item_image.menu_item, self.menu_item)
        self.assertIsNotNone(self.menu_item_image.image)
        self.assertIsNotNone(self.menu_item_image.created_on)
        self.assertIsNotNone(self.menu_item_image.updated_on)

    def test_menu_item_image_str(self):
        self.assertEqual(str(self.menu_item_image),
                         str(self.menu_item_image.id))


class MenuItemTagTestCase(TestCase):

    def setUp(self):
        self.menu_item_tag = MenuItemTag.objects.create(name='Test Tag')

    def test_menu_item_tag_creation(self):
        self.assertTrue(isinstance(self.menu_item_tag, MenuItemTag))
        self.assertEqual(self.menu_item_tag.name, 'Test Tag')
        self.assertIsNotNone(self.menu_item_tag.created_on)
        self.assertIsNotNone(self.menu_item_tag.updated_on)

    def test_menu_item_tag_str(self):
        self.assertEqual(str(self.menu_item_tag), 'Test Tag')

    def test_menu_item_tag_ordering(self):
        menu_item_tag2 = MenuItemTag.objects.create(name='Another Test Tag')
        tags = MenuItemTag.objects.all()
        self.assertEqual(tags[0], menu_item_tag2)
        self.assertEqual(tags[1], self.menu_item_tag)


class MenuItemTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test3@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            date_joined=timezone.now()
        )
        self.menu_item_tag = MenuItemTag.objects.create(name='Test Tag')
        self.menu_item = MenuItem.objects.create(
            user_id=self.user,
            name='Test Menu Item',
            description='Test Description',
            category='Test Category',
            price=10.00
        )
        self.menu_item.tags.add(self.menu_item_tag)

    def test_menu_item_creation(self):
        self.assertTrue(isinstance(self.menu_item, MenuItem))
        self.assertEqual(self.menu_item.user_id, self.user)
        self.assertEqual(self.menu_item.name, 'Test Menu Item')
        self.assertEqual(self.menu_item.description, 'Test Description')
        self.assertEqual(self.menu_item.category, 'Test Category')
        self.assertEqual(self.menu_item.price, 10.00)
        self.assertIn(self.menu_item_tag, self.menu_item.tags.all())
        self.assertIsNotNone(self.menu_item.created_on)
        self.assertIsNotNone(self.menu_item.updated_on)

    def test_menu_item_str(self):
        self.assertEqual(str(self.menu_item), 'Test Menu Item')

    def test_menu_item_ordering(self):
        menu_item2 = MenuItem.objects.create(
            user_id=self.user,
            name='Another Test Menu Item',
            description='Another Test Description',
            category='Test Category',
            price=15.00
        )
        items = MenuItem.objects.all()
        self.assertEqual(items[0], menu_item2)
        self.assertEqual(items[1], self.menu_item)


class RatingTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test4@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            date_joined=timezone.now()
        )
        self.menu_item = MenuItem.objects.create(
            user_id=self.user,
            name='Test Menu Item',
            description='Test Description',
            category='Test Category',
            price=10.00
        )
        self.rating = Rating.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            rating=4
        )

    def test_rating_creation(self):
        self.assertTrue(isinstance(self.rating, Rating))
        self.assertEqual(self.rating.user, self.user)
        self.assertEqual(self.rating.menu_item, self.menu_item)
        self.assertEqual(self.rating.rating, 4)
        self.assertIsNotNone(self.rating.created_on)
        self.assertIsNotNone(self.rating.updated_on)

    def test_rating_str(self):
        self.assertEqual(
            str(self.rating), f"Rating by {self.user.email} for {self.menu_item.name}: 4")

    def test_rating_ordering(self):
        rating2 = Rating.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            rating=5
        )
        ratings = Rating.objects.all()
        self.assertEqual(ratings[0], rating2)
        self.assertEqual(ratings[1], self.rating)


class ReviewTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            date_joined=timezone.now()
        )
        self.menu_item = MenuItem.objects.create(
            user_id=self.user,
            name='Test Menu Item',
            description='Test Description',
            category='Test Category',
            price=10.00
        )
        self.rating = Rating.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            rating=4
        )
        self.review = Review.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            rating=self.rating,
            comment='Test Comment'
        )

    def test_review_creation(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.menu_item, self.menu_item)
        self.assertEqual(self.review.rating, self.rating)
        self.assertEqual(self.review.comment, 'Test Comment')
        self.assertIsNotNone(self.review.created_on)
        self.assertIsNotNone(self.review.updated_on)

    def test_review_str(self):
        self.assertEqual(str(
            self.review), f"Review by {self.user.email} for {self.menu_item.name}: Test Comment")

    def test_review_ordering(self):
        review2 = Review.objects.create(
            user=self.user,
            menu_item=self.menu_item,
            rating=self.rating,
            comment='Another Test Comment'
        )
        reviews = Review.objects.all()
        self.assertEqual(reviews[0], review2)
        self.assertEqual(reviews[1], self.review)
