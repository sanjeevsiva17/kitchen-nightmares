from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('task', views.TaskViewSet)

urlpatterns = [
    path("tasks/", include(router.urls))
]
