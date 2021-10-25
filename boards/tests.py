from unittest import mock
import bcrypt
import json
import jwt

from datetime      import date, datetime
from django.test   import TestCase, Client
from django.http   import response
from boards.models import Board, Category, Tag
from users.models  import User
from my_settings   import SECRET_KEY, algorithm
from freezegun     import freeze_time

class PostingTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Category.objects.create(
            id   = 1,
            name = 'category_test'
        )
        
        Tag.objects.create(
            id       = 1,
            name     = "test",
            category = Category.objects.get(id=1)
        )
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            title    = 'testing_title',
            content  = 'testing_content,',
            writer   = User.objects.get(id=1),
            password = hashed_password,
            tag      = Tag.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        
    def test_success_posting(self):

        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title"    : "testing_post_1",
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
        
    def test_fail_not_input_data(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
    def test_fail_same_title_posting(self):
    
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title"    : 'testing_title',
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
    def test_fail_keyerror_posting(self):
    
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title1"   : "testing_post",
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
class PostingDetailTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Category.objects.create(
            id   = 1,
            name = 'category_test'
        )
        
        Tag.objects.create(
            id       = 1,
            name     = "test",
            category = Category.objects.get(id=1)
        )
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            title    = 'testing_title',
            content  = 'testing_content',
            writer   = User.objects.get(id=1),
            password = hashed_password,
            tag      = Tag.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        
    def test_success_posting_list_view(self):
        
        data = [
            {
            "id"        : 1,
            "title"     : 'testing_title',
            "content"   : 'testing_content',
            "hits"      : 1,
            "writer"    : "runningman",
            "tag"       : "test",
        }
            ]

        response = self.client.get('/boards/detail/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message' : data})
        
    def test_fail_invalid_board_id(self):

        response = self.client.get('/boards/detail/1000')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'INVALID_BOARD_ID'})

@freeze_time('2021-10-12 00:00:00')
class PostingListTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Category.objects.create(
            id   = 1,
            name = 'category_test'
        )
        
        Tag.objects.create(
            id       = 1,
            name     = "test",
            category = Category.objects.get(id=1)
        )
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            title    = 'testing_title',
            content  = 'testing_content',
            writer   = User.objects.get(id=1),
            password = hashed_password,
            tag      = Tag.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        
    def test_success_posting_list_view(self):
        
        data = [
            {
            "id"        : 1,
            "title"     : 'testing_title',
            "content"   : 'testing_content',
            "hits"      : 0,
            "writer"    : "runningman",
            "tag"       : "test",
            "create_at" : '2021-10-12 00:00:00'
        }
            ]

        response = self.client.get('/boards/list?limit=1&offset=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message' : data})
        
    def test_fail_value_error(self):
    
        response = self.client.get('/boards/list?limit=&offset=')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : "ENTER page_number"})
        
class PostingListTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Category.objects.create(
            id   = 1,
            name = 'category_test'
        )
        
        Tag.objects.create(
            id       = 1,
            name     = "test",
            category = Category.objects.get(id=1)
        )
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            title    = 'testing_title',
            content  = 'testing_content',
            writer   = User.objects.get(id=1),
            password = hashed_password,
            tag      = Tag.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        
    def test_success_reposting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,
            'title'    : 'modify_test',
            'content'  : 'modify_content',
            'password' : '1234',
            'tag'      : 1
        }
        
        response = self.client.post('/boards/repost/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
        
    def test_fail_not_matched_password_reposting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }
        
        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            "id"       : 1,
            "title"    : "modify_test",
            "content"  : "modify_content",
            "password" : "12",
            'tag'      : 1
        }
        
        response = self.client.post('/boards/repost/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 401)
        
    def test_fail_key_error_reposting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }
        
        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            "id"       : 1,
            # "title"    : "modify_test",
            "content"  : "modify_content",
            "password" : "1234",
            'tag'      : 1
        }
        
        response = self.client.post('/boards/repost/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
class PostingDeleteTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Category.objects.create(
            id   = 1,
            name = 'category_test'
        )
        
        Tag.objects.create(
            id       = 1,
            name     = "test",
            category = Category.objects.get(id=1)
        )
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            title    = 'testing_title',
            content  = 'testing_content',
            writer   = User.objects.get(id=1),
            password = hashed_password,
            tag      = Tag.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        
    def test_success_delete_posting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,  
            'password' : '1234'
        }
        
        response = self.client.post('/boards/delete/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
        
    def test_fail_delete_not_matched_password_posting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,  
            'password' : '123'
        }
        
        response = self.client.post('/boards/delete/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 401)
        
    def test_fail_delele_invalid_board_id_posting(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,  
            'password' : '1234'
        }
        
        response = self.client.post('/boards/delete/10', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
    def test_fail_delele_key_error(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data = {
            'id'       : 1,  
            'passwor' : '1234'
        }
        
        response = self.client.post('/boards/delete/1', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)