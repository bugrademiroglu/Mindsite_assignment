from django.db import models
from jobs.models import Jobs


class ErrorLogs(models.Model):
    text = models.TextField(blank=False, null=False)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='job_process_data')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    def save_log(self, log):
        new_log = ErrorLogs(text=log)
        new_log.save()

    def get_error_logs(self):
        return self.text