from django.urls import path

from . import views

app_name="polls"
urlpatterns = [
    path('list/', views.polls_list, name="list"),
    # polls/details/1/
    path('details/<int:poll_id>/', views.poll_detail, name='detail')
]
