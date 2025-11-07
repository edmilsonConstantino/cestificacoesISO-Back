from django.urls import path
from .views import SubmissionCreateView, SubmissionListView

urlpatterns = [
    path('', SubmissionCreateView.as_view(), name="submission-create"),
    path('list/', SubmissionListView.as_view(), name="submission-list"),
]
