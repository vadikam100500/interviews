# import os

from django.urls import include, path
# from djoser.views import TokenDestroyView
# from dotenv import load_dotenv
# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions, routers
from rest_framework import routers

from api.views import DealViewSet

# load_dotenv()


app_name = 'api'

router = routers.DefaultRouter()
router.register('deals', DealViewSet, basename='deals')


urlpatterns = [
    path('', include(router.urls)),
]


# schema_view = get_schema_view(
#     openapi.Info(
#         title='Foodgram',
#         default_version='v1',
#         description=('Документация для сервиса Foodgram'),
#         contact=openapi.Contact(email=os.getenv('CONTACT_EMAIL')),
#         license=openapi.License(name=os.getenv('LICENSE')),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )


# urlpatterns += [
#     path(
#         'docs/swagger/json',
#         schema_view.without_ui(cache_timeout=0),
#         name='schema-json'
#     ),
#     path(
#         'docs/swagger/',
#         schema_view.with_ui('swagger', cache_timeout=0),
#         name='schema-swagger-ui'
#     ),
# ]
