from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from server.apps.main.views import *

app_name = "main"

router = DefaultRouter()
router.register(r"polls", AdminPollViewSet)
router.register(r"questions", QuestionViewSet)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns_docs = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = urlpatterns_docs + [

    path("active_polls", PollListView.as_view(), name="all_polls"),
    path("", include(router.urls)),
    path("pass_poll", PassPollApi.as_view()),
    path("passed_polls", HistoryApi.as_view()),
]
