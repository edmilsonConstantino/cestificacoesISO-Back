from django.urls import path
from .views import SubmissionCreateView


#essa parte e de Urls que eu defini e a tall tall
urlpatterns = [
    path("submissions/", SubmissionCreateView.as_view(), name="submission-create"),
]