from datasets.models import Dataset, PersonalDataset, Rating
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from os import path
import json

# Testing
from unittest import skip

files_url = path.join(settings.MEDIA_ROOT, 'test')

# Status codes: http://www.django-rest-framework.org/api-guide/status-codes

def readFile(filename):
    datapath = path.join(files_url, filename)
    f = file(datapath)
    return SimpleUploadedFile(f.name, f.read())

def create_dataset(title, about, filename, extension):
    return {
        "title": title,
        "about": about,
        "data": readFile(filename),
        "extension": extension
    }   

def cleanDatasets():
    datasets = Dataset.objects.all()
    for data in datasets:
        data.data.delete(False)
    datasets.delete()

def cleanPersonalDatasets():
    personals = PersonalDataset.objects.all()
    for data in personals:
        data.personal_data.delete(False)
    personals.delete()

# LIST, RETRIEVE
@skip("Don't want to test")
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
        self.assertEqual(len(content), 2)
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
        self.assertEqual(len(content), 2)
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
@skip("Don't want to test")
class DatasetTest(APITestCase):
    @classmethod
    def setUpClass(self):
        super(DatasetTest, self).setUpClass()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword') 
        User.objects.create_user('jair', 'jair@dce.com', 'jairpassword')

    def tearDown(self):
        cleanDatasets()

    def test_dataset_create_1(self):
        dataset_2 = create_dataset("TimeSeries", "tseries", "tseries_test.csv", 1)
        
        self.client.login(username='jair', password='jairpassword')
        response = self.client.post(reverse('dataset-list'), dataset_2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Dataset.objects.all().delete()

    def test_dataset_create_2(self):
        dataset_1 = create_dataset("Bitly", "", "usagov_test.txt", 2)
 
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse('dataset-list'), dataset_1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Dataset.objects.all().delete()

    def test_dataset_delete_1(self):
        dataset_1 = create_dataset("Bitly", "", "usagov_test.txt", 2)
 
        self.client.login(username='john', password='johnpassword')
        self.client.post(reverse('dataset-list'), dataset_1)

        self.assertEqual(Dataset.objects.count(), 1)
        id = Dataset.objects.all()[0].id

        response = self.client.delete(reverse('dataset-detail', args=[id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 
    def test_dataset_delete_2(self):

        dataset_1 = create_dataset("Bitly", "", "usagov_test.txt", 2)
        
        self.client.login(username='john', password='johnpassword')
        self.client.post(reverse('dataset-list'), dataset_1)
        self.client.logout()

        self.assertEqual(Dataset.objects.count(), 1)
        id = Dataset.objects.all()[0].id

        self.client.login(username='jair', password='jairpassword')
        response = self.client.delete(reverse('dataset-detail', args=[id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# POST, DELETE
@skip("Don't want to test")
class PersonalDatasetTest(APITestCase):
    @classmethod
    def setUpClass(self):
        super(PersonalDatasetTest, self).setUpClass()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword') 
        User.objects.create_user('jair', 'jair@dce.com', 'jairpassword')

    def setUp(self):

        dataset_1 = create_dataset("Bitly", "", "usagov_test.txt", 2)
        dataset_2 = create_dataset("TimeSeries", "tseries", "tseries_test.csv", 1)
               
        self.client.login(username='jair', password='jairpassword')
        self.client.post(reverse('dataset-list'), dataset_2)
        self.client.logout()

        self.client.login(username='john', password='johnpassword')
        self.client.post(reverse('dataset-list'), dataset_1)
        self.client.logout()

    def tearDown(self):
        cleanPersonalDatasets()
        cleanDatasets()

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

