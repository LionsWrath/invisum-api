from datasets.models import Dataset, PersonalDataset, Rating
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework_jwt import utils
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from unittest import skip
from os import path
import json

files_url = path.join(settings.MEDIA_ROOT, 'test')

# Status codes: http://www.django-rest-framework.org/api-guide/status-codes

def readFile(filename):
    datapath = path.join(files_url, filename)
    f = file(datapath)
    return SimpleUploadedFile(f.name, f.read(), content_type='multipart/form-data')

def create_dataset(title, about, filename, extension):
    return {
        "title": title,
        "about": about,
        "data": readFile(filename),
        "extension": extension
    }   

class BaseTestCase(APITestCase):
    def make_login(self, username, password):
        return self.client.login(username=username, password=password) 

    def make_jwt_login(self, user):
        payload = utils.jwt_payload_handler(user)
        return utils.jwt_encode_handler(payload)

    def create_header(self, token):
        return 'JWT {0}'.format(token)

    def create_authorization(self, user):
        token = self.make_jwt_login(user)
        return { 'HTTP_AUTHORIZATION': self.create_header(token) }

    def setUp(self):
        self.user_1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword') 
        self.user_2 = User.objects.create_user('jair', 'jair@dce.com', 'jairpassword')

class UserTest(BaseTestCase):
    def test_login(self):
        login = self.make_login('john', 'johnpassword') 
        self.assertTrue(login) 

    def test_login_jwt(self):
	data = {
	    'username': 'john',
	    'password': 'johnpassword'
	}
	response = self.client.post(reverse('jwt_login'), data)
	self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        response = self.client.get(reverse('user-list'), format='json')
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 2)

    def test_retrieve(self):
        id = User.objects.all()[0].id
        name = User.objects.all()[0].username

        response = self.client.get(reverse('user-detail', args=[id]))
        content = json.loads(response.content)

        self.assertEqual(content['username'], name)

    def test_list_logged(self):
        self.make_login('john', 'johnpassword') 
        response = self.client.get(reverse('user-list'), format='json')
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 2)

    def test_retrieve_logged(self):
        id = User.objects.all()[0].id
        name = User.objects.all()[0].username

        self.make_login('john', 'johnpassword')  
        response = self.client.get(reverse('user-detail', args=[id]))
        content = json.loads(response.content)

        self.assertEqual(content['username'], name)

class DatasetTestCreate(BaseTestCase):
    def test_dataset_create_jwt(self):
        dataset_2 = create_dataset("TimeSeries", "tseries", "tseries_test.csv", 1)
        
        auth = self.create_authorization(self.user_1)
        
        response = self.client.post(reverse('dataset-list'), dataset_2, **auth)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dataset_create_normal(self):
        dataset_1 = create_dataset("Bitly", "", "usagov_test.txt", 2)
 
        self.make_login('john', 'johnpassword')
        response = self.client.post(reverse('dataset-list'), dataset_1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class DatasetTestDelete(BaseTestCase):
    def setUp(self):
        super(DatasetTestDelete, self).setUp()
        dataset_1 = create_dataset("Bitly", "", "usagov_test.txt", 2)
 
        auth = self.create_authorization(self.user_1)
        self.client.post(reverse('dataset-list'), dataset_1, **auth)
        self.id = Dataset.objects.all()[0].id

    def test_dataset_delete_success(self):
        auth = self.create_authorization(self.user_1)

        response = self.client.delete(reverse('dataset-detail', args=[self.id]), **auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 
    def test_dataset_delete_fail(self):
        auth = self.create_authorization(self.user_2)

        response = self.client.delete(reverse('dataset-detail', args=[self.id]), **auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PersonalDatasetBaseTest(BaseTestCase):
    def setUp(self):
        super(PersonalDatasetBaseTest, self).setUp()

        dataset_1 = create_dataset("Bitly", "", "usagov_test.txt", 2)
        dataset_2 = create_dataset("TimeSeries", "tseries", "tseries_test.csv", 1)
               
        self.make_login('jair', 'jairpassword')
        self.client.post(reverse('dataset-list'), dataset_2)
        self.client.logout()

        self.make_login('john', 'johnpassword')
        self.client.post(reverse('dataset-list'), dataset_1)
        self.client.logout()

        self.data = { "description": "pdataset" }
        
        self.id_1 = Dataset.objects.all()[0].id
        self.id_2 = Dataset.objects.all()[1].id

class PersonalDatasetTestCreate(PersonalDatasetBaseTest):
    def test_personal_create_jwt(self):
        auth = self.create_authorization(self.user_1)
        
        response = self.client.post(reverse('personal-create', args=[self.id_1]), self.data, **auth)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_personal_create_normal(self):
        self.make_login('jair', 'jairpassword')

        response = self.client.post(reverse('personal-create', args=[self.id_2]), self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PersonalDatasetTestDelete(PersonalDatasetBaseTest):
    def setUp(self):
        super(PersonalDatasetTestDelete, self).setUp()

        auth = self.create_authorization(self.user_1)
        request = self.client.post(reverse('personal-create', args=[self.id_1]), self.data, **auth)
        self.id = PersonalDataset.objects.all()[0].id

    def test_personal_delete_success(self):
        self.make_login('john', 'johnpassword')

        response = self.client.delete(reverse('personal-detail', args=[self.id])) 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 
    def test_personal_delete_2(self):
        self.make_login('jair', 'jairpassword')

        response = self.client.delete(reverse('personal-detail', args=[self.id])) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RatingTest(APITestCase):
    pass

class FeedTest(APITestCase):
    pass

class DataProcessingTest(APITestCase):
    pass

