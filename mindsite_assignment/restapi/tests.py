from users.models import Users
from jobs.models import Jobs
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime

#TODO: ResumeJob, Stopjob, CancelJob endpointleri multiprocessing üzerinden sağlıklı şekilde
#TODO: tamamlandıktan sonra testi yazılacak.

#TODO: Testler iyileştirilecek.

class CreateUserTest(APITestCase):
    def setUp(self):
      
        self.data = {'name': 'bugra', 'surname': 'demiroglu', 'title': 'developer'}

    def test_can_create_user(self):
        response = self.client.post(reverse('get-user-list-view'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

class ReadUserTest(APITestCase):
    def setUp(self):
        self.user = Users.objects.create(name="bugra")

    def test_can_read_user_list(self):
        response = self.client.get(reverse("get-user-list-view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateJobTest(APITestCase):
    def setUp(self):
        user = Users.objects.create(name="Bugra",surname="Demiroglu",title="Developer")
        self.data = {'status': 'Running', 
                                 'start_time': datetime.datetime.now(),
                                 'end_time': datetime.datetime.now(),
                                 "job_type":"Product matching",
                                 "job_name":"testjob",
                                 "user":user.id
                                }

    def test_can_create_job(self):
        response = self.client.post(reverse('create-job-view'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ListJobTest(APITestCase):
    def test_can_list_job(self):
        response = self.client.get(reverse("job-list-view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetLogAllTest(APITestCase):
    def test_can_create_job(self):
        response = self.client.get(reverse("get-all-logs-view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSpecificJobLogTest(APITestCase):
    def setUp(self):
        user = Users.objects.create(name="Bugra",surname="Demiroglu",title="Developer")
        self.job = Jobs.objects.create(status="Running",
                                start_time=datetime.datetime.now(),
                                end_time=datetime.datetime.now(),
                                job_type="Product matching",
                                job_name="testjob",
                                user=user
                                )

    def test_can_get_specific_job_log(self):
        response = self.client.get(reverse("get-logs-view", args=[self.job.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetDetailedJobLogTest(APITestCase):
    def setUp(self):
        user = Users.objects.create(name="Bugra",surname="Demiroglu",title="Developer")
        self.job = Jobs.objects.create(status="Running",
                                start_time=datetime.datetime.now(),
                                end_time=datetime.datetime.now(),
                                job_type="Product matching",
                                job_name="testjob",
                                user=user
                                )

    def test_can_get_detailed_job_log(self):
        response = self.client.get(reverse("get-detailed-job-view", args=[self.job.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetFinishedJobsTest(APITestCase):
    def setUp(self):
        user = Users.objects.create(name="Bugra",surname="Demiroglu",title="Developer")
        Jobs.objects.create(status="Success",
                            start_time=datetime.datetime.now(),
                            end_time=datetime.datetime.now(),
                            job_type="Product matching",
                            job_name="testjob",
                            user=user,
                            finished=True
                            )

    def test_can_get_finished_job(self):
        response = self.client.get(reverse("get-finished-job-view"))
        response_data = response.json()
        if (response_data[0]["finished"] == True):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            return status.HTTP_404_NOT_FOUND


class GetLastJobsTest(APITestCase):
    def setUp(self):
        self.user = Users.objects.create(name="Bugra",surname="Demiroglu",title="Developer")
        Jobs.objects.create(status="Running",
                            start_time=datetime.datetime.now(),
                            end_time=datetime.datetime.now(),
                            job_type="Product matching",
                            job_name="getlastjobtest",
                            user=self.user,
                            finished=True
                            )

    def test_can_get_last_jobs(self):
        response = self.client.get(reverse("last-job-view", args=[self.user.name]))
        response_data = response.json()
        if (response_data[0]["job_name"] == "getlastjobtest"):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            return status.HTTP_404_NOT_FOUND


class GetRunningJobsTest(APITestCase):
    def setUp(self):
        user = Users.objects.create(name="Bugra",surname="Demiroglu",title="Developer")
        self.job = Jobs.objects.create(status="Running",
                            start_time=datetime.datetime.now(),
                            end_time=datetime.datetime.now(),
                            job_type="Product matching",
                            job_name="testjob",
                            user=user,
                            finished=False
                            )

    def test_can_get_running_jobs(self):
        job = Jobs.objects.get(id=self.job.id)
        response = self.client.get(reverse("running-job-view"))
        response_data = response.json()
        if (response_data[0]["status"] == "Running" and response_data[0]["finished"] == False):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            return status.HTTP_404_NOT_FOUND


class RestartJobViewTest(APITestCase):
    def setUp(self):
        user = Users.objects.create(name="Bugra",surname="Demiroglu",title="Developer")
        self.job = Jobs.objects.create(progress=False,
                            status="Success",
                            start_time=datetime.datetime.now(),
                            end_time=datetime.datetime.now(),
                            job_type="Product matching",
                            job_name="testjob",
                            user=user,
                            finished=True
                            )

    def test_can_restart_jobs(self):
        response = self.client.get(reverse("restart-job-view", args=[self.job.id]))
        response_data = response.json()
        if (response_data[0]["status"] == "Finished" and response_data[0]["finished"] == True
        and response_data[0]["progress"] == False):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            return status.HTTP_404_NOT_FOUND
