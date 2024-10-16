import { Routes } from '@angular/router';
import { LoginLayoutComponent } from './layouts/login-layout/login-layout.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProfileComponent } from './profile/profile.component';
import { InventoryComponent } from './inventory/inventory.component';

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
          { path: 'profile', component: ProfileComponent }
        ]
      },
      { path: '**', redirectTo: 'login' }  // Redirect to login if unknown route
];
