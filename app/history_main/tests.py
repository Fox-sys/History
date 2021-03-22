from django.test import TestCase, Client
from .models import SolderPost, Exhibit, MainUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

def tests_decorator(func):
    def wrapper(self):
        print('\n----------------------------------------------------------------------')
        func(self)
    return wrapper


class SoldertestCase(TestCase):
    def setUp(self):
        self.client = Client(username="test", password="135790asz")
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.user = MainUser.objects.create_user(
            username='test',
            password='135790asz'
        )
        for i in range(22):
            SolderPost.objects.create(
                creator=MainUser.objects.get(username='test'),
                first_name="hzhz",
                middle_name="hzhz",
                last_name="hzhz",
                desc="hzhz",
                is_alive=True,
                birth_date="1111-11-11",
                photo=SimpleUploadedFile('hzhz.jpg', content=b'', content_type='image/jpg')
            )

    @tests_decorator
    def test_solder_list(self):
        """
            Just testing main page of site
        """
        response = self.client.get(reverse('index'))
        print(response.status_code, reverse('index'))

    @tests_decorator
    def test_solder_pager(self):
        """
            Here is test of pager system.
            With standart settings should print 3 pages and 1 404 error
        """
        for i in range(1, 5):
            response = self.client.get(f"{reverse('index')}?page={i}")
            print(response.status_code, f"{reverse('index')}?page={i}")
    
    @tests_decorator
    def test_solder_detail(self):
        for i in range(2):
            response = self.client.get(reverse('solder_detail', kwargs={"pk": 22*2+i}))
            print(response.status_code, reverse('solder_detail', kwargs={"pk": 22*2+i}))

    @tests_decorator
    def test_solder_create(self):
        pass

