from datasets.models import Dataset, PersonalDataset, Rating
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from os import path

files_url = path.join(settings.MEDIA_ROOT, 'test')

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

# POST
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
        self.assertEqual(Dataset.objects.count(), 1)

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
        self.assertEqual(Dataset.objects.count(), 1)

# 403 error for not logged (FORBIDDEN)
# 400 error for malformed request (BAD RESQUEST)
# POST
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
    
    

class RatingTest(APITestCase):
    pass

class FeedTest(APITestCase):
    pass

class DataProcessingTest(APITestCase):
    pass

