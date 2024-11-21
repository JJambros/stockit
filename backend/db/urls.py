from django.urls import path
from .views import auth_views, audit_views, order_views, search_views, profile_views, shipment_views, supplier_views, dashboard_views, inventory_views, forecasting_views, shipping_address_views  # Import the views

urlpatterns = [

# --- AUTH --- # 

    # Authentication URLs
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Register User URL
    path('register/', auth_views.register_user, name='register'),
    
    # Change Password URL
    path('update-password/', auth_views.update_password, name='update-password'),


# --- PROFILE --- #

    # Profile URL (viewing/updating the logged-in user's profile)
    path('profile/', profile_views.user_profile_detail, name='profile-detail'),


# --- INVENTORY --- #

    # Inventory URLs
    path('inventory/', inventory_views.inventory_list, name='inventory-list'),  # List and create inventory items
    path('inventory/<int:pk>/', inventory_views.inventory_detail, name='inventory-detail'),  # Get, update, delete specific item

    # Inventory Category URLs
    path('inventory-categories/', inventory_views.inventory_category_list, name='category-list'),
    path('inventory-categories/<int:pk>/', inventory_views.inventory_category_detail, name='category-detail'),


# --- SEARCH --- #

    # Search URLs 
    path('search/', search_views.search_view, name='search'),


# --- DASHBOARD --- #

    path('dashboard/', dashboard_views.dashboard_list, name='dashboard-list'),  # List and create dashboard entries
    path('dashboard/<int:pk>/', dashboard_views.dashboard_detail, name='dashboard-detail'),  # Get, update, delete dashboard entry

    # Net Sales
    path('dashboard/net-sales/', dashboard_views.dashboard_net_sales, name='dashboard-net-sales'),

    # Total Orders 
    path('dashboard/total-orders/', dashboard_views.dashboard_total_orders, name='dashboard-total-orders'),

    # Net Purchases by Category
    path('dashboard/net-purchases-by-category/', dashboard_views.dashboard_net_purchases_by_category, name='dashboard-net-purchases-by-category'),

    # Net Purchases by Item
    path('dashboard/net-purchases-by-item/', dashboard_views.dashboard_net_purchases_by_item, name='dashboard-net-purchases-by-item'),

    # Breakdown
    path('dashboard/total-breakdown/', dashboard_views.dashboard_total_breakdown, name='dashboard-total-breakdown'),


# --- FORECASTING --- # 

    # Inventory Forecasting URLs
    path('inventory/forecast/<int:inventory_id>/<str:forecast_date>/', forecasting_views.inventory_forecast, name='inventory-forecast'),
    path('forecasting/adjust/', forecasting_views.adjust_forecast, name='forecast-adjust'),

    # ForecastingPreferences URLs
    path('forecasting-preferences/', forecasting_views.forecasting_preferences_list, name='forecasting-preferences-list'),
    path('forecasting-preferences/<int:pk>/', forecasting_views.forecasting_preferences_detail, name='forecasting-preferences-detail'),


# --- AUDIT TRAIL --- # 

    # Audit Trail URLs
    path('audit-trails/', audit_views.audit_trail_list, name='audit-trail-list'),  # List all audit trail entries

# --- SALES ORDERS --- # 

    # CustomerOrder URLs --> SalesOrders
    path('sales-orders/', order_views.sales_order_list, name='customer-order-list'),
    path('sales-orders/<int:pk>/', order_views.sales_order_detail, name='customer-order-detail'),

    # Order Items URLs
    path('order-items/', order_views.sales_order_item_list, name='order-item-list'),  # List all order items

    # Index URLs
    path('index/', order_views.index_view, name='index-view'),

    # OrderStatus URLs
    path('order-status/', order_views.order_status_list, name='order-status-list'),
    path('order-status/<int:pk>/', order_views.order_status_detail, name='order-status-detail'),


# --- SHIPPING ADDRESS --- # 

    # Location URLs --> ShippingAddress
    path('Shipping-Address/', shipping_address_views.shipping_address_list, name='location-list'),
    path('Shipping-Address/<int:pk>/', shipping_address_views.shipping_address_detail, name='location-detail'),


# --- SHIPMENT --- # 

    # Shipment related URLs
    path('shipments/', shipment_views.sales_order_shipment_list, name='shipment-list'),  # List and create shipments
    path('shipments/<int:pk>/', shipment_views.sales_order_shipment_detail, name='shipment-detail'),  # Retrieve, update, delete specific shipment
        # --- Marked order as shipped --- #
    path('orders/<int:order_id>/mark_shipped/', shipment_views.mark_order_as_shipped, name='mark-order-shipped'), # Endpoint to mark an order as shipped


# --- SUPPLIER --- # 

    # Supplier URLs
    path('suppliers/', supplier_views.supplier_list, name='supplier-list'),
    path('suppliers/<int:pk>/', supplier_views.supplier_detail, name='supplier-detail'),

    # Purchase Order URLs
    path('purchase-orders/', supplier_views.purchase_order_list, name='purchase-order-list'),
    path('purchase-orders/<int:pk>/', supplier_views.purchase_order_detail, name='purchase-order-detail'),
]