from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import TestView

router = SimpleRouter()

urlpatterns = [
    path('dudos', TestView.as_view()),
]

