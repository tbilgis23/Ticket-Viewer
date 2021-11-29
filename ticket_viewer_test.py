from unittest import mock, TestCase
import ticket_viewer as tv
import os
import requests as req
import io


class TestTicketViewer(TestCase):
    @mock.patch.dict(os.environ, {"SUBDOMAIN": "test", "USER_EMAIL": "test", "PASSWORD": "test"})
    def test_get_json(self):
        self.assertEqual(tv.get_json(), "error")

    @mock.patch.dict(os.environ, {"SUBDOMAIN": os.environ.get("SUBDOMAIN"), "USER_EMAIL": 
    os.environ.get("USER_EMAIL"), "PASSWORD": os.environ.get("PASSWORD")})
    def test_get_json2(self):
        subdomain = os.environ.get('SUBDOMAIN')
        url = f"https://{subdomain}.zendesk.com/api/v2/tickets"
        user_email = os.environ.get("USER_EMAIL")
        password = os.environ.get('PASSWORD')
        response = req.get(url, auth=(user_email, password))
        self.assertEqual(tv.get_json(), response.json())
    
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_view_all(self, mock_stdout):
        tv.view_all()
        file_1 = open("view_all.stdout").readlines()
        file_str = "".join(file_1)
        self.assertEqual(mock_stdout.getvalue(), file_str)
        self.assertEqual(tv.view_all(), "menu")
    
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_view_all2(self, mock_stdout):
        tv.view_all()
        file_1 = open("view_all_2.stdout").readlines()
        file_str = "".join(file_1)
        self.assertEqual(mock_stdout.getvalue(), file_str)
    
    @mock.patch("builtins.input", side_effect=["1", "quit"])
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_view_ticket(self, mock_stdout, mock_input):
        tv.view_ticket()
        file_1 = open("view_ticket.stdout").readlines()
        file_str = "".join(file_1)
        self.assertEqual(file_str, mock_stdout.getvalue())
    
    @mock.patch("builtins.input", side_effect=["sdf", "quit"])
    @mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_view_ticket2(self, mock_stdout, mock_input):
        self.assertEqual(tv.view_ticket(), "menu")
    



