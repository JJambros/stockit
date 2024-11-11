from django.urls import path
from . import views  # Import the views from the db app

urlpatterns = [
    # Example view (keeping in case we need it for testing)
    path('data/', views.my_data, name='db-data'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile URL (viewing/updating the logged-in user's profile)
    path('profile/', views.profile_detail, name='profile-detail'),

    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory-list'),  # List and create inventory items
    path('inventory/<int:pk>/', views.inventory_detail, name='inventory-detail'),  # Get, update, delete specific item

    # Category URLs
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),

    # Search URLs 
    path('search/', views.search_view, name='search'),

    # Dashboard Related URLs
    path('dashboard/', views.dashboard_list, name='dashboard-list'),  # List and create dashboard entries
    path('dashboard/<int:pk>/', views.dashboard_detail, name='dashboard-detail'),  # Get, update, delete dashboard entry
        # --- Net Sales --- #
    path('dashboard/net-sales/', views.dashboard_net_sales, name='dashboard-net-sales'),
        # --- Total Orders --- #
    path('dashboard/total-orders/', views.dashboard_total_orders, name='dashboard-total-orders'),
        # --- Net Purchases by Category --- #
    path('dashboard/net-purchases-by-category/', views.dashboard_net_purchases_by_category, name='dashboard-net-purchases-by-category'),
        # --- Net Purchases by Item --- #
    path('dashboard/net-purchases-by-item/', views.dashboard_net_purchases_by_item, name='dashboard-net-purchases-by-item'),
        # --- Breakdown --- #
    path('dashboard/total-breakdown/', views.dashboard_total_breakdown, name='dashboard-total-breakdown'),


    # Inventory Forecasting URLs
    path('inventory/forecast/<int:inventory_id>/<str:forecast_date>/', views.inventory_forecast, name='inventory-forecast'),

    # ForecastingPreferences URLs
    path('forecasting-preferences/', views.forecasting_preferences_list, name='forecasting-preferences-list'),
    path('forecasting-preferences/<int:pk>/', views.forecasting_preferences_detail, name='forecasting-preferences-detail'),

    # Index URLs
    path('index/', views.index_view, name='index-view'),

    # Audit Trail URLs
    path('audit-trails/', views.audit_trail_list, name='audit-trail-list'),  # List all audit trail entries

    # Order Items URLs
    path('order-items/', views.order_item_list, name='order-item-list'),  # List all order items

    # CustomerOrder URLs
    path('customer-orders/', views.customer_order_list, name='customer-order-list'),
    path('customer-orders/<int:pk>/', views.customer_order_detail, name='customer-order-detail'),

    # Shipment related URLs
    path('shipments/', views.shipment_list, name='shipment-list'),  # List and create shipments
    path('shipments/<int:pk>/', views.shipment_detail, name='shipment-detail'),  # Retrieve, update, delete specific shipment
        # --- Marked order as shipped --- #
    path('orders/<int:order_id>/mark_shipped/', views.mark_order_as_shipped, name='mark-order-shipped'), # Endpoint to mark an order as shipped

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier-list'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier-detail'),
]