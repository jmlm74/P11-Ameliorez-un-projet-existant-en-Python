from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
import inspect

from user_app.models import User


class TestUser(TestCase):
    """
    Test the creation - connection and disconnection of a user
    Use the Client class from django to act as a dummy web browser
    """

    def setUp(self):
        """"
        Setup method --> initialize django client and create test-user
        """
        user = User.objects.create(username='foobar', email='foobar@team.fr')
        user.set_password('foobar')
        user.save()
        self.user = user
        self.c = Client()

    def tearDown(self):
        """
        Teardown method --> not used here
        """
        pass

    def test_user_creation(self):
        """
        Create user by the Post to /user_app/user
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post('/user_app/login', {'email': 'toto@tutu.com',
                                                           'password': 'jmlm7485',
                                                           'confirm_password': 'jmlm7485', })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_connection(self):
        """
        User Connection through the login view
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.c.post('/user_app/login', {'email': 'foobar@team.fr',
                                                  'password': 'foobar',
                                                  'connexion': 'connexion',
                                                  'connexion_creation': 'connexion', })
        self.assertEquals(response.status_code, 302)  # redirect to /index --> return 200 if not logged-in
        self.assertEquals(response.url, '/home_app/index/')

    def test_user_disconnection(self):
        """
        Logout
        """
        print(inspect.currentframe().f_code.co_name)
        self.client.login(username='foobar', password='foobar')
        response = self.c.get(reverse('user_app:ulogout'))
        self.assertEquals(response.status_code, 302)


class Testchangepassword(TransactionTestCase):
    """
    Test save and remove bookmark view (Ajax)
    """

    def setUp(self):
        super(Testchangepassword, self).setUpClass()
        self.client = Client()
        # user creation
        user = User.objects.create(username='foobar')
        user.set_password('foobar')
        user.save()
        self.user = user
        self.c = Client()


    def test_change_password_ok(self):
        """
        Test changing password is ok --> Connection is OK with new password
        """
        print(inspect.currentframe().f_code.co_name)
        self.client.login(username='foobar', password='foobar')
        response = self.client.post(reverse('user_app:change_password'), {'old_password': 'foobar',
                                                                          'new_password1': 'afgt45tYl',
                                                                          'new_password2': 'afgt45tYl'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Your password was successfully updated!")
        response = self.c.get(reverse('user_app:ulogout'))
        self.assertEquals(response.status_code, 302)
        response = self.c.post('/user_app/login', {'email': 'foobar@team.fr',
                                                   'password': 'afgt45tYl',
                                                   'connexion': 'connexion',
                                                   'connexion_creation': 'connexion', })
        self.assertEquals(response.status_code, 302)  # redirect to /index --> return 200 if not logged-in


    def test_change_password_notconnected_notok(self):
        """
        Verify the change password with no user connected is redirected
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.client.post(reverse('user_app:change_password'))
        self.assertEquals(response.status_code, 302)


