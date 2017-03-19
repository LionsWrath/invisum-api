from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

class UserTest(APITestCase):
    @classmethod
    def setUpClass(self):
        super(UserTest, self).setUpClass()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword') 
        User.objects.create_user('jair', 'jair@dce.com', 'jairpassword')
    
    def test_login(self):
        login = self.client.login(username='john', password='johnpassword') 
        self.assertTrue(login) 

    def test_list(self):
        response = self.client.get(reverse('user-list'), format='json')

        data = '[{"id":1,"email":"lennon@thebeatles.com","username":"john","datasets":[]},{"id":2,"email":"jair@dce.com","username":"jair","datasets":[]}]' 
        self.assertEqual(response.content, data)

    def test_retrieve(self):
        response = self.client.get(reverse('user-detail', args=[1]))

        data = '{"id":1,"email":"lennon@thebeatles.com","username":"john","datasets":[]}'
        self.assertEqual(response.content, data)

    def test_list_logged(self):
        login = self.client.login(username='john', password='johnpassword') 
        response = self.client.get(reverse('user-list'), format='json')

        data = '[{"id":1,"email":"lennon@thebeatles.com","username":"john","datasets":[]},{"id":2,"email":"jair@dce.com","username":"jair","datasets":[]}]' 
        self.assertEqual(response.content, data)

    def test_retrieve_logged(self):
        login = self.client.login(username='john', password='johnpassword')  
        response = self.client.get(reverse('user-detail', args=[1]))

        data = '{"id":1,"email":"lennon@thebeatles.com","username":"john","datasets":[]}'
        self.assertEqual(response.content, data)

class DatasetTest(APITestCase):
    pass

class RatingTest(APITestCase):
    pass

class FeedTest(APITestCase):
    pass

class DataProcessingTest(APITestCase):
    pass

