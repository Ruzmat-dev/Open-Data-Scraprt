from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # 🔹 Admin panel
    path('admin/', admin.site.urls),

    # 🔹 Jobs app’ning barcha endpointlari shu yerdan boshlanadi:
    #     http://127.0.0.1:8000/jobs/
    path('jobs/', include('jobs.urls')),

    # 🔹 OpenAPI schema va Swagger/Redoc hujjatlar
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
