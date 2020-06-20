# Client object is considered as a dummy Web browser
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
# reverse -> get url name fro urls.py and return actual url Ex:/foo/
from django.urls import reverse


class AdminSiteTest(TestCase):
    """This method is run before executing any test_ method"""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='password123',
            name='Test user'
        )

    def test_user_list_in_django_admin(self):
        """
        admin site user listview,
        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#reversing-admin-urls
        """
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)  # get all data from user list page

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        # url : EX: /admin/core/user/2
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
