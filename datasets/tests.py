from datasets.models import Dataset, PersonalDataset, Rating
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from os import path
import json

files_url = path.join(settings.MEDIA_ROOT, 'test')

# Status codes: http://www.django-rest-framework.org/api-guide/status-codes

# LIST, RETRIEVE
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
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content[0]['username'], 'john')
        self.assertEqual(content[1]['username'], 'jair')

    def test_retrieve(self):
        id = User.objects.all()[0].id
        name = User.objects.all()[0].username

        response = self.client.get(reverse('user-detail', args=[id]))
        content = json.loads(response.content)

        self.assertEqual(content['username'], name)

    def test_list_logged(self):
        self.client.login(username='john', password='johnpassword') 
        response = self.client.get(reverse('user-list'), format='json')
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content[0]['username'], 'john')
        self.assertEqual(content[1]['username'], 'jair')

    def test_retrieve_logged(self):
        id = User.objects.all()[0].id
        name = User.objects.all()[0].username

        self.client.login(username='john', password='johnpassword')  
        response = self.client.get(reverse('user-detail', args=[id]))
        content = json.loads(response.content)

        self.assertEqual(content['username'], name)

# POST, DELETE
class DatasetTest(APITestCase):
    @classmethod
    def setUpClass(self):
        super(DatasetTest, self).setUpClass()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword') 
        User.objects.create_user('jair', 'jair@dce.com', 'jairpassword')

    def test_dataset_create_1(self):
        datapath = path.join(files_url, 'tseries_test.csv')
        f = file(datapath)
        dataset_data_2 = {
            "title": "TimeSeries file",
            "about": "tseries",
            "data": SimpleUploadedFile(f.name, f.read()),
            "extension": 1
        }
        
        self.client.login(username='jair', password='jairpassword')
        response = self.client.post(reverse('dataset-list'), dataset_data_2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dataset_create_2(self):
        datapath = path.join(files_url, 'usagov_test.txt')
        f = file(datapath)
        dataset_data_1 = {
            "title": "Bitly data from USA government",
            "about": "",
            "data": SimpleUploadedFile(f.name, f.read()),
            "extension": 2
        }

        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse('dataset-list'), dataset_data_1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dataset_delete_1(self):
        datapath = path.join(files_url, 'usagov_test.txt')
        f = file(datapath)
        dataset_data_1 = {
            "title": "Bitly data from USA government",
            "about": "",
            "data": SimpleUploadedFile(f.name, f.read()),
            "extension": 2
        }

        self.client.login(username='john', password='johnpassword')
        self.client.post(reverse('dataset-list'), dataset_data_1)

        self.assertEqual(Dataset.objects.count(), 1)
        id = Dataset.objects.all()[0].id

        response = self.client.delete(reverse('dataset-detail', args=[id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 
    def test_dataset_delete_2(self):
        datapath = path.join(files_url, 'usagov_test.txt')
        f = file(datapath)
        dataset_data_1 = {
            "title": "Bitly data from USA government",
            "about": "",
            "data": SimpleUploadedFile(f.name, f.read()),
            "extension": 2
        }

        self.client.login(username='john', password='johnpassword')
        self.client.post(reverse('dataset-list'), dataset_data_1)
        self.client.logout()

        self.assertEqual(Dataset.objects.count(), 1)
        id = Dataset.objects.all()[0].id

        self.client.login(username='jair', password='jairpassword')
        response = self.client.delete(reverse('dataset-detail', args=[id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# POST, DELETE
class PersonalDatasetTest(APITestCase):
    @classmethod
    def setUpClass(self):
        super(PersonalDatasetTest, self).setUpClass()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword') 
        User.objects.create_user('jair', 'jair@dce.com', 'jairpassword')

    def setUp(self):

        datapath = path.join(files_url, 'usagov_test.txt')
        f = file(datapath)
        dataset_data_1 = {
            "title": "Bitly data from USA government",
            "about": "",
            "data": SimpleUploadedFile(f.name, f.read()),
            "extension": 2
        }
        
        datapath = path.join(files_url, 'tseries_test.csv')
        f = file(datapath)
        dataset_data_2 = {
            "title": "TimeSeries file",
            "about": "tseries",
            "data": SimpleUploadedFile(f.name, f.read()),
            "extension": 1
        }
        
        self.client.login(username='jair', password='jairpassword')
        self.client.post(reverse('dataset-list'), dataset_data_2)
        self.client.logout()

        self.client.login(username='john', password='johnpassword')
        self.client.post(reverse('dataset-list'), dataset_data_1)
        self.client.logout()

    def tearDown(self):
        Dataset.objects.all().delete()

    def test_personal_create_1(self):
        data = { "description": "pdataset" }

        self.assertEqual(Dataset.objects.count(), 2)
        id = Dataset.objects.all()[0].id

        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse('personal-create', args=[id]), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_personal_create_2(self):
        data = { "description": "pdataset" }

        self.assertEqual(Dataset.objects.count(), 2)
        id = Dataset.objects.all()[1].id

        self.client.login(username='jair', password='jairpassword')
        response = self.client.post(reverse('personal-create', args=[id]), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # A user try to delete a PersonalDataset
    def test_personal_delete_1(self):
        data = { "description": "pdataset" }

        self.assertEqual(Dataset.objects.count(), 2)
        id = Dataset.objects.all()[0].id

        self.client.login(username='jair', password='jairpassword')
        self.client.post(reverse('personal-create', args=[id]), data)
        
        self.assertEqual(PersonalDataset.objects.count(), 1)
        id = PersonalDataset.objects.all()[0].id

        response = self.client.delete(reverse('personal-detail', args=[id])) 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 
    # Another user try to delete a PersonalDataset
    def test_personal_delete_2(self):
        data = { "description": "pdataset" }

        self.assertEqual(Dataset.objects.count(), 2)
        id = Dataset.objects.all()[0].id

        self.client.login(username='jair', password='jairpassword')
        self.client.post(reverse('personal-create', args=[id]), data)
        self.client.logout()
        
        self.assertEqual(PersonalDataset.objects.count(), 1)
        id = PersonalDataset.objects.all()[0].id

        self.client.login(username='john', password='johnpassword')
        response = self.client.delete(reverse('personal-detail', args=[id])) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RatingTest(APITestCase):
    pass

class FeedTest(APITestCase):
    pass

class DataProcessingTest(APITestCase):
    pass

