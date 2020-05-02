from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('task', views.TaskViewSet)
router.register('taskstate', views.TaskStateViewSet)

urlpatterns = [
    path("tasks/", include(router.urls)),
]
