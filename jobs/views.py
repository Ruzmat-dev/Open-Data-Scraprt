from rest_framework import generics, filters
from django.http import JsonResponse
from .models import Job
from .serializers import JobSerializer

# Oddiy JSON chiqazish (test uchun)
def job_list(request):
    jobs = Job.objects.all().values('title', 'company', 'location', 'posted_at')
    return JsonResponse(list(jobs), safe=False)

# ✅ REST API uchun DRF klasslar
class JobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-posted_at')
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "company", "description"]
    #
    # def get_object(self):
    #     obj = super().get_object()
    #     date = self.request.query_params.get('date')


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
