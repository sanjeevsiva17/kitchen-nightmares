from django.db import models
from django.contrib.auth import get_user_model
from rabbitmq.send import publish


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Task, self).save(force_insert, force_update, using, update_fields)
        TaskObj = {}
        TaskObj["id"] = self.id
        TaskObj["title"] = self.title
        TaskObj["priority"] = self.priority
        if self.priority == self.HIGH:
            priority = 3
        elif self.priority == self.MEDIUM:
            priority = 2
        else:
            priority = 1
        TaskObj["created_by"] = self.created_by.id
        TaskObj["is_active"] = self.is_active
        publish(TaskObj, priority)


class TaskState(TimeStampMixin):
    NEW = 'NEW'
    ACCEPTED = 'ACC'
    COMPLETED = 'COM'
    DECLINED = 'DEC'
    CANCELED = 'CAN'

    STATES_CHOICES = [(NEW, 'NEW'), (ACCEPTED, 'ACCEPTED'), (COMPLETED, 'COMPLETED'), (DECLINED, 'LOW'),
                      (CANCELED, 'CAN')]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    state = models.CharField(
        default=NEW,
        choices=STATES_CHOICES,
        max_length=3
    )
