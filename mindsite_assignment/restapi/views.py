import re
from users.models import Users
from jobs.models import Jobs
from .serializers import JobSerializerCreate, ErrorLogSerializer, JobSerializerList, UserSerializerList
from rest_framework import generics
from logerrors.models import ErrorLogs
from rest_framework.response import Response
import multiprocessing
from multiprocessing import Process
from rest_framework import throttling

#TODO: Cancel stop resume process simulasyon kismi kaldi
#TODO: Unit testler kaldi
#TODO: Documantation kaldi
#TODO: Github heroku deploy etmek kaldi

class JobList(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can list all the jobs with using /getjobs endpoint"""
    queryset = Jobs.objects.all()
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)


class CreateJobs(generics.CreateAPIView, throttling.ScopedRateThrottle):
    """You can create and start new job with using /createjob endpoint"""
    serializer_class = JobSerializerCreate
    queryset = Jobs.objects.all()

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)


class CancelJob(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can cancel a specific job with using /canceljob/{int:job_id} endpoint"""
    queryset = Jobs.objects.all()
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)

    def list(self, request, job_id):
        try:
            queryset = Jobs.objects.filter(id=job_id)
            job = Jobs.objects.get(id=job_id)
        except:
            return Response("Searching jobs does not exist. Try existing one.")
        result = job.cancel_job_process()
        if result is False:
            return Response("That job has already been cancelled or failed.")
        ErrorLogs.objects.create(job=job, text="The job has been cancelled by the user.")
        serializer = JobSerializerList(queryset, many=True)
        return Response(serializer.data)


class StopJob(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can stop a specific job with using /stopjob/{int:job_id} endpoint"""
    queryset = Jobs.objects.all()
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)

    def list(self, request, job_id):
        try:
            queryset = Jobs.objects.filter(id=job_id)
            job = Jobs.objects.get(id=job_id)
        except:
            return Response("Searching jobs does not exist. Try existing one.")
        result = job.stop_job()
        if result is False:
            return Response("That job has already been cancelled or failed.")
        ErrorLogs.objects.create(job=job, text="The job has been stopped by the user.")
        serializer = JobSerializerList(queryset, many=True)
        return Response(serializer.data)


class ResumeJob(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can resume a stopped job with using /resumejob/{int:job_id} endpoint"""
    queryset = Jobs.objects.all()
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)

    def list(self, request, job_id):
        try:
            queryset = Jobs.objects.filter(id=job_id)
            job = Jobs.objects.get(id=job_id)
        except:
            return Response("Searching jobs does not exist. Try existing one.")
        result = job.resume_job()
        if result is False:
            return Response("You cannnot resume unstarted job.")
        ErrorLogs.objects.create(job=job, text="The job is running.")
        serializer = JobSerializerList(queryset, many=True)
        return Response(serializer.data)


class RestartJob(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can restart a job which was failed or stopped by something with using /restart/{int:job_id} endpoint"""
    queryset = Jobs.objects.all()
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)

    def list(self, request, job_id):
        try:
            queryset = Jobs.objects.filter(id=job_id)
            job = Jobs.objects.get(id=job_id)
        except:
            return Response("Searching jobs does not exist. Try existing one.")

        job.restart_job()
        ErrorLogs.objects.create(job=job, text="The job has been restarted.")
        serializer = JobSerializerList(queryset, many=True)
        return Response(serializer.data)


class ListRunningJobs(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can list all the running jobs with using /runningjobs"""
    queryset = Jobs.objects.filter(status="Running")
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)


class LastTenJobs(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can list specified user's last ten jobs according to the created date with using /lastjobs/{str:user_name} endpoint"""
    queryset = Jobs.objects.all()
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)

    def list(self, request, user_name):
        user = Users.objects.get(name=user_name)
        queryset = Jobs.objects.filter(user=user).order_by('-id')[:10]
        serializer = JobSerializerList(queryset, many=True)
        return Response(serializer.data)


class GetFinishedJobs(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can list all the finished jobs with using /getfinishedhjobs endpoint"""
    queryset = Jobs.objects.filter(finished=True)
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)


class GetDetailedJobInfo(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can get detailed log info about specified job with using /getdetailedjob/{int:job_id} endpoint"""
    queryset = Jobs.objects.all()
    serializer_class = JobSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)

    def list(self, request, job_id):
        queryset = Jobs.objects.get(id=job_id)
        serializer = JobSerializerList(queryset, many=False)
        return Response(serializer.data)


class GetLogs(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can get logs only for specified job with using /getlogs/{int:job_id} endpoint"""
    queryset = ErrorLogs.objects.all()
    serializer_class = ErrorLogSerializer

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)

    def list(self, request, job_id):
        try:
            queryset = ErrorLogs.objects.filter(job=job_id)
            job = Jobs.objects.get(id=job_id)
            ErrorLogs.objects.create(job=job, text="The job log searched.")
        except:
            return Response("Searching jobs does not exist. Try existing one.")

        serializer = ErrorLogSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAllLogs(generics.ListAPIView, throttling.ScopedRateThrottle):
    """You can get all the logs which were created before if you are curious with using /getalllogs endpoint"""
    queryset = ErrorLogs.objects.all()
    serializer_class = ErrorLogSerializer

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)


class UserList(generics.ListCreateAPIView, throttling.ScopedRateThrottle):
    """You can list and create users with using /userlist endpoint"""
    queryset = Users.objects.all()
    serializer_class = UserSerializerList

    throttle_scope = "request_count"
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        
        return super().allow_request(request, view)