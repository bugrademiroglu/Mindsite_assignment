from django.db import models
from users.models import Users
import time
from multiprocessing import Process


class Jobs(models.Model):

    STATUS = (
       ("Success", "Success"),
       ("Running", "Running"),
       ("Cancelled", "Cancelled"),
       ("Stopped", "Stopped"),
       ("Failed", "Failed")
   )

    JOB_TYPES = (
        ("Product matching", "Product matching job"),
        ("Hourly price comparison", "Hourly price comparison job"),
        ("Rating - review tracking", "Rating - review tracking job"),
        ("Competition analysis", "Competition analysis job"),
        ("Buybox tracking", "Buybox tracking job"),
    )

    progress = models.BooleanField(default=False)
    status = models.CharField(max_length=255,
                              choices=STATUS
                             )
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    job_type = models.TextField(choices=JOB_TYPES)
    job_name = models.CharField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users',)
    finished = models.BooleanField(default=False)

    pids_list = []

    def __str__(self):
        return "JobProcess" + self.job_name + str(self.id)

    def _get_pids(self):
        """ Inner function which is responsible to terminate running process
        """
        if len(Jobs.pids_list) > 0:
            p = Jobs.pids_list.pop()
            p.terminate()


    def _save_processing_jobs(self,p):
        """Inner function which is save the current process job in to the global list variable

        Args:
            p (Process): [Running process]
        """
        Jobs.pids_list.append(p)

    def job_processing(self, seconds):
        """When a job is created or restarted that method calls simulate the long running jobs

        Args:
            seconds (string): [Time to sleep]
        """
        sec = int(seconds)
        time.sleep(sec)
        self.finished = True
        self.progress = False
        self.status = "Success"
        self.save()

    def start_job_process(self):
        """When a job is created or restarted that method calls in order to start new process
        """
        seconds = (self.end_time-self.start_time).seconds
        # operationalerror disk i/o error hatasi alindi :(
        p = Process(target=self.job_processing, args=[str(seconds)])
        # p = Process(target=self.job_processing(seconds))
        p.start()
        self._save_processing_jobs(p)

    def get_detailed_job_info(self):
        """That method prepare an information about specified job by the user.

        Returns:
            [dict]: [Information about a specified job]
        """
        detailed_information = {
                                "progress":self.progress,
                                "status": self.status,
                                "start_time": self.start_time,
                                "end_time": self.end_time,
                                "created": self.created,
                                "user": self.user,
                                "finished": self.finished,
        }
        return detailed_information

    def cancel_job_process(self):
        """If user use that endpoint with specific job id then specified job will be terminate

        Returns:
            [Boolean]: [In case of not getting Failed or Cancelled the jobs status return False]
        """
        if self.status is not "Failed" or self.status is not "Cancelled":
            self.status = "Cancelled"
            self.progress = False
            self.save()
            self._get_pids()
        else:
            return False
    
    def stop_job(self):
        """If user use that endpoint with specific job id then specified job will be stopped

        Returns:
            [Boolean]: [In case of not getting Failed or Cancelled the jobs status return False]
        """
        if self.status is not "Failed" or self.staus is not "Cancelled":
            self.status = "Stopped"
            self.save()
            if len(Jobs.pids_list) > 0:
                p = Jobs.pids_list.pop()
                if p.is_alive():
                    p.close()
                    p.join()
        else:
            return False
    
    def resume_job(self):
        """If user use that endpoint with specific job id then specified job will be resume

        Returns:
            [Boolean]: [In case of not getting Stopped or Running the jobs status return False]
        """
        if self.status is "Stopped":
            self.status = "Running"
            self.save()
        else:
            return False
    
    def restart_job(self):
        """If user use that endpoint with specific job id then specified job will be restarted
        by calling start_job_process method
        """
        self.start_job_process()
