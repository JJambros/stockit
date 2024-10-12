from django.urls import path
from . import views  # Import the views from the db app

urlpatterns = [
    path('data/', views.my_data, name='db-data'),  # Example view for the db app
]
