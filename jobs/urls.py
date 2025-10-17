from django.urls import path
from .views import job_list, JobListView, JobDetailView

urlpatterns = [
    path('', job_list, name='job-list'),  # oddiy Json chiqazuvchi funksiya
    path('jobs/', JobListView.as_view(), name='job-list-api'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
]
