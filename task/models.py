from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TimeStampMixin):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'

    PRIORITY_CHOICES = [(HIGH, 'HIGH'), (MEDIUM, 'MEDIUM'), (LOW, 'LOW')]

    title = models.CharField(max_length=250)
    priority = models.CharField(
        choices=PRIORITY_CHOICES,
        max_length=1
    )
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class TaskState(TimeStampMixin):
    NEW = 'NEW'
    ACCEPTED = 'ACC'
    COMPLETED = 'COM'
    DECLINED = 'DEC'
    CANCELED = 'CAN'

    STATES_CHOICES = [(NEW, 'NEW'), (ACCEPTED, 'ACCEPTED'), (COMPLETED, 'COMPLETED'), (DECLINED, 'LOW'), (CANCELED, 'CAN')]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    state = models.CharField(
        choices=STATES_CHOICES,
        max_length=3
    )
