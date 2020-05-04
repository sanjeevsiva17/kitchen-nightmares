from django.db import models
from django.contrib.auth import get_user_model
from rabbitmq.send import publish
from django_fsm import FSMField, transition
from redis_notifications.notifications import setDeclined


# Create your models here

HIGH = 'H'
MEDIUM = 'M'
LOW = 'L'

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

    STATES_CHOICES = [(NEW, 'NEW'), (ACCEPTED, 'ACCEPTED'), (COMPLETED, 'COMPLETED'), (DECLINED, 'DECLINED'),
                      (CANCELED, 'CANCELED')]

    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    state = FSMField(
        default=NEW,
        choices=STATES_CHOICES,
    )

    @transition(field=state, source=NEW, target=ACCEPTED)
    def accepted(self):
        print(self.ACCEPTED)
        pass

    @transition(field=state, source=ACCEPTED, target=COMPLETED)
    def completed(self):
        print(self.COMPLETED)
        pass

    @transition(field=state, source=ACCEPTED, target=NEW)
    def declined(self):
        TaskObj = {}
        TaskObj["id"] = self.task.id
        TaskObj["title"] = self.task.title
        TaskObj["priority"] = self.task.priority
        if self.task.priority == HIGH:
            priority = 3
        elif self.task.priority == MEDIUM:
            priority = 2
        else:
            priority = 1
        TaskObj["created_by"] = self.task.created_by.id
        TaskObj["is_active"] = self.task.is_active
        setDeclined(str(TaskObj["id"]), str(TaskObj["title"]))
        publish(TaskObj, priority)
        print(self.DECLINED)

    @transition(field=state, source=[NEW, ACCEPTED], target=CANCELED)
    def canceled(self):
        print(self.CANCELED)
        pass
