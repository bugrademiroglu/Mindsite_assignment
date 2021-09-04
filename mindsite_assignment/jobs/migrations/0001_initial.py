# Generated by Django 3.2.6 on 2021-09-02 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Success', 'The job is completed.'), ('Running', 'The job has been running.'), ('Cancelled', 'The job has been cancelled.'), ('Stopped', 'The job has been stopped.'), ('Failed', 'The job is failed.')], max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True)),
                ('job_type', models.TextField(choices=[('Product matching', 'Product matching job'), ('Hourly price comparison', 'Hourly price comparison job'), ('Rating - review tracking', 'Rating - review tracking job'), ('Competition analysis', 'Competition analysis job'), ('Buybox tracking', 'Buybox tracking job')])),
                ('job_name', models.CharField(max_length=255)),
                ('finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.users')),
            ],
        ),
    ]