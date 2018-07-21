from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateOrder, ManageOrder

urlpatterns = [
    url(r'createorder/', CreateOrder.as_view()),
    url(r'manageorder/(?P<pk>[0-9]+)/', ManageOrder.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)