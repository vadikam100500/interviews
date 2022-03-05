import os

from django.urls import include, path
from dotenv import load_dotenv
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from . import views

load_dotenv()

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', views.CustomUserViewSet, basename='users')
router.register('mailings', views.MailingViewSet, basename='mailings')
router.register('messages', views.MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.urls')),
]


schema_view = get_schema_view(
    openapi.Info(
        title='Fabrique',
        default_version='v1',
        description=('Документация для сервиса Fabrique'),
        contact=openapi.Contact(email=os.getenv('CONTACT_EMAIL')),
        license=openapi.License(name=os.getenv('LICENSE')),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns += [
    path(
        'docs/json',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]
