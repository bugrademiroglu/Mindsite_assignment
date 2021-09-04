from rest_framework import serializers
from jobs.models import Jobs
from logerrors.models import ErrorLogs
from users.models import Users
from rest_framework.response import Response
from random import randint
import time
from users.models import Users
from multiprocessing import Process, process


class ErrorLogSerializer(serializers.ModelSerializer):
    "Getting logs for specified job"
    text = serializers.PrimaryKeyRelatedField(
        required=False, queryset=ErrorLogs.objects.all().select_related("text"))
    class Meta:
        model = ErrorLogs
        fields = [
            "text",
            "created",
        ]


class JobSerializerCreate(serializers.ModelSerializer):

    user = serializers.DjangoModelField()

    class Meta:
        model = Jobs
        fields = [
            "id",
            "status",
            "created",
            "start_time",
            "end_time",
            "job_type",
            "job_name",
            "user",
        ]
        extra_kwargs = {
            "progress": {"required": False},
        }

    def create(self, validated_data):
        user = validated_data["user"]
        job_name = validated_data["job_name"]
        start_time = validated_data["start_time"]
        end_time = validated_data["end_time"]
        time_left = end_time - start_time

        value = randint(0, 10000)

        try:
            user_obj = Users.objects.get(name=user)
        except Users.DoesNotExist:
            raise serializers.ValidationError("The user is not exist on the system. Try existing one")

        validated_data["user"] = user_obj
        validated_data["job_name"] = "JobProcess" + str(job_name) + str(value)
        validated_data["status"] = "Running"
        validated_data["progress"] = True

        new_job = Jobs.objects.create(**validated_data)

        ErrorLogs.objects.create(text="The job is created.", job=new_job)
        new_job.start_job_process()
        ErrorLogs.objects.create(text="The job finished succesfully.", job=new_job)
        return new_job


class JobSerializerList(serializers.ModelSerializer):

    user = serializers.CharField(source="user.name")

    class Meta:
        model = Jobs
        fields = [
            "id",
            "progress",
            "status",
            "created",
            "start_time",
            "end_time",
            "job_type",
            "job_name",
            "user",
            "finished",
        ]


class UserSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = [
            "id",
            "name",
            "surname",
            "title",
        ]

