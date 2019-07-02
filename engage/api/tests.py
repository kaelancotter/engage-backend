from engage import settings
from engage.ingest.models import Agenda, Committee, Tag, AgendaItem, EngageUserProfile, Message
from engage.api.utils import send_mail
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import datetime
import json
import jwt
import os

# Create your tests here.
class TestAgendasEndpoint(TestCase):


    def test_response(self):
        response = self.client.get("/api/agendas.json")
        self.assertEqual(200, response.status_code)
        json_res = response.json()
        self.assertEqual([], json_res['results'])

    def test_db(self):
        committee = Committee(name="test")
        committee.save()
        Agenda(meeting_time=393939393, committee=committee).save()
        response = self.client.get("/api/agendas.json")
        self.assertEqual(200, response.status_code)
        result_dict = response.json()
        self.assertEqual(1, len(result_dict['results']))


class TestTagsEndpoint(TestCase):
    def test_response(self):
        response = self.client.get("/api/tags.json")
        self.assertEqual(200, response.status_code)
        from engage.ingest.management.commands.populate_tags import seed_tags
        #we just want to make sure that we have atleast the seed tags in the db
        self.assertGreaterEqual(len(seed_tags), len(response.json()))

class TestLoginEndpoint(TestCase):


    def test_user_creation(self):
        user_to_test_against = User.objects.create_user("test", email="test@test.com", password='test')
        jwt_token = jwt.encode({'email':user_to_test_against.email}, settings.SECRET_KEY)
        response = self.client.post("/api/login.json", {'email':'test@test.com', 'password': 'test'})
        token = response.json()['token']
        #have to decode the jwt_token since it will be a byte-object and not string
        self.assertEqual(jwt_token.decode('utf-8'), token)

    def test_user_wrong_info(self):
        user_to_test_against = User.objects.create_user("test", email="test@test.com", password='test')
        response = self.client.post("/api/login.json", {'email':'test@test.com', 'password': 'testing'})
        self.assertEqual(404, response.status_code)


    def test_user_signup(self):
        user_info = {
            "first_name": "Test",
            "last_name": "Testman",
            "username": "test_testman",
            "email": "test@test.com",
            "password": "test"
        }
        response = self.client.post("/api/signup/", user_info )
        self.assertEqual(201, response.status_code)
        user = User.objects.get(email="test@test.com")
        self.assertEqual(user_info['email'], user.email)

class TestAgendasByTagEndpoint(TestCase):
    def test_response(self):
        tag = Tag(name="Test")
        tag.save()
        committee = Committee(name="Council")
        committee.save()
        agenda = Agenda(meeting_time=949494949, committee=committee)
        agenda.save()
        agenda_item = AgendaItem(title="test", department="test", agenda=agenda )
        agenda_item.save()
        agenda_item.tags.add(tag)
        agenda_item.save()
        response = self.client.get("/api/tag/Test/agenda/items/")
        self.assertEqual(200, response.status_code)
        self.assertEqual("Test", response.json()['tag'])
        self.assertEqual(1, len(response.json()['items']))
        self.assertEqual("test", response.json()['items'][0]['title'])


class TestSendMessageEndpoint(TestCase):
    def setUp(self):
        user = User.objects.create_user("test", email="test@test.com", password="test")
        self.engage_user = EngageUserProfile(user=user)
        self.engage_user.save()
        committee = Committee(name="test")
        committee.save()
        self.agenda = Agenda(meeting_time=393939393, committee=committee)
        self.agenda.save()
        self.ag_item = AgendaItem(title="test", department="test", agenda=self.agenda)
        self.ag_item.save()
    def test_response(self):
        self.client.login(username="test@test.com", password="test")
        response = self.client.post("/api/add/message/", data=json.dumps({
                "token": "faketoken123",
                "committee": "test",
                "pro": 4,
                "content":"I support that",
                "ag_item":self.ag_item.pk}), content_type="application/json")
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(Message.objects.all()))
        sent_message = Message.objects.first()
        self.assertEqual("test@test.com", sent_message.user.email)
        self.assertEqual(0, sent_message.sent)

    '''
    Add SES test
    '''
    def test_mail_util_func(self):
        if os.environ.get("ENGAGE_BACKEND_NO_MAIL") == 'TRUE':
            # Early Exit for CI runners without valid MAIL API KEY
            return
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        static = 'PDF_Reports'
        full_path = os.path.join(root_dir, static)
        attachment_file_path = str(full_path) + "/test_pdf_report.pdf"
        print(attachment_file_path)
        result = send_mail({'user': {'email': 'engage@engage.town'}, 'subject': 'test', 'content': '<html><body>Testing</body></html>', 'attachment_file_path': attachment_file_path, 'attachment_file_name': 'test_pdf_report.pdf'})
        self.assertTrue(result)
