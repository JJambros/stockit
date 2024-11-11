import { Routes } from '@angular/router';
import { AuthGuard } from './auth.guard';
import { LoginLayoutComponent } from './layouts/login-layout/login-layout.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProfileComponent } from './profile/profile.component';
import { InventoryComponent } from './inventory/inventory.component';
import { AuditComponent } from './audit/audit.component';
import { OrderComponent } from './order/order.component';
import { OrdersSummayComponent } from './quick_links/orders-summay/orders-summay.component';
import { CustomerOrderComponent } from './quick_links/customer-order/customer-order.component';
import { SuppliersComponent } from './quick_links/suppliers/suppliers.component';
import { ItemsComponent } from './quick_links/items/items.component';
import { CompanyPageComponent } from './company-page/company-page.component';

export const routes: Routes = [
    {
        path: '',
        component: LoginLayoutComponent, // No navbar for login layout
        children: [
          { path: 'login', component: LoginComponent }
        ]
      },
      {
        path: '',
        component: MainLayoutComponent, // Navbar for main layout
        children: [
          { path: 'dashboard', component: DashboardComponent },
          { path: 'inventory', component: InventoryComponent },
          { path: 'profile', component: ProfileComponent },
          { path : 'audit', component: AuditComponent},
          { path: 'profile', component: ProfileComponent},
          { path: 'order', component: OrderComponent},
          {path: 'orders-summary', component: OrdersSummayComponent},
          {path: 'customer-order', component: CustomerOrderComponent},
          {path: 'suppliers', component: SuppliersComponent},
          {path: 'itemList', component: ItemsComponent},
          {path: 'company-page', component: CompanyPageComponent},
        ]
      },
      { path: '**', redirectTo: 'login' }  // Redirect to login if unknown route
];
