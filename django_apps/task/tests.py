"""
Tests for the task app: endpoints, logical deletion, validations,
authentication (JWT-protected) and audit trail (simple_history).
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from django_apps.task.models import Task, TaskStatus

User = get_user_model()


def future(days=1):
    return (timezone.now() + timedelta(days=days)).isoformat()


class TaskEndpointsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="pass1234",
            first_name="Owner",
            last_name="User",
        )
        self.client.force_authenticate(user=self.user)

    def _create_task(self, **overrides):
        payload = {
            "title": "Write report",
            "description": "Quarterly report",
            "due_date": future(3),
        }
        payload.update(overrides)
        return self.client.post(reverse("task_create"), payload, format="json")

    # --- authentication -------------------------------------------------

    def test_write_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self._create_task()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_read_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_token_endpoint_returns_access_and_refresh(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "owner@example.com", "password": "pass1234"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # --- creation & validations ----------------------------------------

    def test_create_task_sets_author_from_request_user(self):
        response = self._create_task()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["created_by"], self.user.id)
        self.assertEqual(response.data["status"], TaskStatus.PENDING)
        task = Task.objects.get(id=response.data["id"])
        self.assertEqual(task.created_by, self.user)

    def test_create_task_rejects_past_due_date(self):
        response = self._create_task(due_date=future(-2))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_rejects_invalid_status(self):
        response = self._create_task(status="urgent")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- listing / deletion --------------------------------------------

    def test_list_excludes_logically_deleted(self):
        task_id = self._create_task().data["id"]
        self._create_task(title="Second")

        self.client.delete(reverse("task_detail", args=[task_id]))

        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["results"]]
        self.assertNotIn("Write report", titles)
        self.assertIn("Second", titles)

    def test_logical_delete_keeps_row(self):
        task_id = self._create_task().data["id"]
        response = self.client.delete(reverse("task_detail", args=[task_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        task = Task.objects.get(id=task_id)
        self.assertFalse(task.is_active)
        self.assertIsNotNone(task.deleted_at)

    def test_change_status(self):
        task_id = self._create_task().data["id"]
        response = self.client.patch(
            reverse("task_change_status", args=[task_id]),
            {"status": TaskStatus.COMPLETED},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], TaskStatus.COMPLETED)

    def test_update_not_found_returns_404(self):
        response = self.client.patch(
            reverse("task_detail", args=[9999]),
            {"title": "Nope"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- upcoming -------------------------------------------------------

    def test_upcoming_window(self):
        self._create_task(title="Soon", due_date=future(2))
        self._create_task(title="Later", due_date=future(30))

        response = self.client.get(reverse("task_upcoming"), {"days": 7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("Soon", titles)
        self.assertNotIn("Later", titles)

    def test_upcoming_excludes_completed(self):
        task_id = self._create_task(title="Soon", due_date=future(2)).data["id"]
        self.client.patch(
            reverse("task_change_status", args=[task_id]),
            {"status": TaskStatus.COMPLETED},
            format="json",
        )
        response = self.client.get(reverse("task_upcoming"))
        titles = [item["title"] for item in response.data["results"]]
        self.assertNotIn("Soon", titles)

    # --- filters --------------------------------------------------------

    def test_filter_by_status_and_search(self):
        self._create_task(title="Buy milk", description="groceries")
        done_id = self._create_task(title="Deploy").data["id"]
        self.client.patch(
            reverse("task_change_status", args=[done_id]),
            {"status": TaskStatus.POSTPONED},
            format="json",
        )

        by_status = self.client.get(
            reverse("task_list"), {"status": TaskStatus.POSTPONED}
        )
        titles = [item["title"] for item in by_status.data["results"]]
        self.assertEqual(titles, ["Deploy"])

        by_search = self.client.get(reverse("task_list"), {"search": "milk"})
        titles = [item["title"] for item in by_search.data["results"]]
        self.assertEqual(titles, ["Buy milk"])

    # --- audit trail (simple_history) ----------------------------------

    def test_history_records_who_changed_the_task(self):
        editor = User.objects.create_user(
            email="editor@example.com", password="pass1234"
        )
        task_id = self._create_task().data["id"]

        # A different authenticated user changes the status.
        self.client.force_authenticate(user=editor)
        self.client.patch(
            reverse("task_change_status", args=[task_id]),
            {"status": TaskStatus.COMPLETED},
            format="json",
        )

        response = self.client.get(reverse("task_history", args=[task_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Most recent first: the change by the editor, then the creation.
        self.assertEqual(response.data[0]["history_type"], "Changed")
        self.assertEqual(response.data[0]["history_user"], "editor@example.com")
        self.assertEqual(response.data[-1]["history_type"], "Created")
        self.assertEqual(response.data[-1]["history_user"], "owner@example.com")

    def test_history_not_found_returns_404(self):
        response = self.client.get(reverse("task_history", args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
