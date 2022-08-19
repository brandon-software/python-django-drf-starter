from ast import NotEq
import json
from django.urls import reverse
from nose.tools import ok_, eq_, assert_not_equal
from rest_framework.test import APITestCase
from rest_framework import status

from users.test.factories import UserFactory
from src.taskapi.models import Task
import uuid


class TestAnonymousTaskDetailTestCase(APITestCase):
    """
    Tests anonymous user task list operations.
    """

    def setUp(self):
        pass

    def test_retreive_alltasks_with_no_data_and_no_user_fails(self):
        self.url = reverse('task-list') + 'alltasks' + '/'
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retreive_tasks_with_no_data_and_no_user_fails(self):
        self.url = reverse('task-list')
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)


class TestTaskDetail_withNoTask_TestCase(APITestCase):
    """
    Tests task list operations with no task setup.
    """

    def setUp(self):
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.data = {
            "created_by": self.user.id,
            "title": "string3",
            "content": "string3",
            "created_on": "2022-07-30",
            "due_date": "2022-07-30",
        }

    def test_task_model(self):
        title = 'string4'
        myobject = Task(title=title, created_by_id=self.user.id)
        eq_(title, str(myobject))

    def test_post_request_with_no_data_and_no_user_fails(self):
        response = self.client.post(reverse('task-list'), {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retreive_non_existing_task_with_no_user(self):
        self.taskid = 1
        self.changeurl = reverse('task-list') + str(self.taskid) + '/'
        response = self.client.get(self.changeurl, format='json')
        eq_(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retreive_non_existing_task_with_no_user(self):
        response = self.client.post(reverse('task-list'), self.data, format='json')
        eq_(response.status_code, status.HTTP_201_CREATED, 'Unable to create a task')


class TestTaskDetail_withTask_TestCase(APITestCase):
    """
    Tests task list operations with task setup.
    """

    def setUp(self):
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.data = {
            "created_by": self.user.id,
            "title": "string3",
            "content": "string3",
            "created_on": "2022-07-30",
            "due_date": "2022-07-30",
        }
        response = self.client.post(reverse('task-list'), self.data, format='json')
        eq_(response.status_code, status.HTTP_201_CREATED, 'Unable to create a task')
        self.taskid = response.json()['id']

    def test_owner_can_change_task(self):
        updatedData = {"title": "string4", "content": "string4", "due_date": "2022-07-31"}
        self.changeurl = reverse('task-list') + str(self.taskid) + '/'
        response = self.client.patch(self.changeurl, updatedData, format='json')
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.json()['title'], updatedData['title'])

    def test_alltasks_request(self):
        self.changeurl = reverse('task-list') + 'alltasks' + '/'
        response = self.client.get(self.changeurl, format='json')
        eq_(response.status_code, status.HTTP_200_OK)

    def test_anonymous_alltasks_request(self):
        self.client.logout()
        self.changeurl = reverse('task-list') + 'alltasks' + '/'
        response = self.client.get(self.changeurl, format='json')
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_owner_can_not_change_other_user_task(self):
        originalpk = self.user.pk
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        assert_not_equal(originalpk, self.user.pk)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        updatedData = {"title": "string4", "content": "string4", "due_date": "2022-07-31"}
        self.changeurl = reverse('task-list') + str(self.taskid) + '/'
        response = self.client.patch(self.changeurl, updatedData, format='json')
        eq_(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_owner_can_retrieve_other_user_task(self):
        self.changeurl = reverse('task-list') + str(self.taskid) + '/'
        response = self.client.get(self.changeurl, format='json')
        eq_(response.status_code, status.HTTP_200_OK, "Owner has retreive task access")

        originalpk = self.user.pk
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        assert_not_equal(originalpk, self.user.pk, 'Users should be different')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.changeurl = reverse('task-list') + str(self.taskid) + '/'
        response = self.client.get(self.changeurl, format='json')
        eq_(response.status_code, status.HTTP_200_OK, "Non-Owner has no retreive access to other user's task")

    def test_anonymous_user_can_not_retreive_existing_task(self):
        self.client.logout()
        self.changeurl = reverse('task-list') + str(self.taskid) + '/'
        response = self.client.get(self.changeurl, format='json')
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)  # , "Anonymous users have retrieve task access")


class TestTaskDetailTestCase(APITestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        self.user = UserFactory()
        tokens = self.user.get_tokens()
        access_token = tokens['access']
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.data = {
            "created_by": self.user.id,
            "title": "string3",
            "content": "string3",
            "created_on": "2022-07-30",
            "due_date": "2022-07-30",
        }
        response = self.client.post(reverse('task-list'), self.data, format='json')
        eq_(response.status_code, status.HTTP_201_CREATED)
        self.taskid = response.json()['id']

    def test_get_request_returns_a_given_id(self):
        self.url = reverse('task-detail', kwargs={'pk': self.taskid})
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_user(self):
        self.url = reverse('task-detail', kwargs={'pk': self.taskid})
        updatedData = {"title": "string4", "content": "string4", "due_date": "2022-07-31"}
        response = self.client.put(self.url, updatedData)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.json()['title'], updatedData['title'])
