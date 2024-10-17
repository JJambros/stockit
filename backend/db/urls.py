from django.urls import path
from . import views  # Import the views from the db app

urlpatterns = [
    # Example view (keeping in case we need it for testing)
    path('data/', views.my_data, name='db-data'),

    # Profile URL (viewing/updating the logged-in user's profile)
    path('profile/', views.profile_detail, name='profile-detail'),

    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory-list'),  # List and create inventory items
    path('inventory/<int:pk>/', views.inventory_detail, name='inventory-detail'),  # Get, update, delete specific item

    # Dashboard URLs
    path('dashboard/', views.dashboard_list, name='dashboard-list'),  # List and create dashboard entries
    path('dashboard/<int:pk>/', views.dashboard_detail, name='dashboard-detail'),  # Get, update, delete dashboard entry

    # Inventory Forecasting URLs
    path('inventory/forecast/<int:inventory_id>/<str:forecast_date>/', views.inventory_forecast, name='inventory-forecast'),
]