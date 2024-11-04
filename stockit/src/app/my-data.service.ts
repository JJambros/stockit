import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MyDataService {
  private apiUrl = 'http://localhost:8000/api/data/';  // Django API URL
  private profileUrl = 'http://localhost:8000/api/profile/';
  private auditUrl = 'http://localhost:8000/api/audit-trails/';
  private orderUrl = 'http://localhost:8000/api/shipments/';
  private inventoryUrl = 'http://localhost:8000/api/inventory/';
  private dashboardOrders = 'http://localhost:8000/api/dashboard/total-orders/';
  private dashboardNetSales = 'http://localhost:8000/api/dashboard/net-sales/';
  private dashboardCategorySort = 'http://localhost:8000/api/dashboard/net-purchases-by-category/';
  private dashboardItemSort = 'http://localhost:8000/api/dashboard/net-purchases-by-item/';
  constructor(private http: HttpClient) { }

    getData(): Observable<any> {
      return this.http.get(this.apiUrl);
    } 

    getUserProfile(): Observable<any> {
      return this.http.get(this.profileUrl);
    }

    getAudit(): Observable<any>{
      return this.http.get(this.auditUrl);
    }

    getOrders(): Observable<any>{
      return this.http.get(this.orderUrl);
    }

    getInventory(): Observable<any>{
      return this.http.get(this.inventoryUrl);
    }

    getDashboardOrders(params: string): Observable<any> {
      return this.http.get(this.dashboardOrders, { params: { time_frame: params } });
    }

    getDashboardNetSales(params: string): Observable<any> {
      return this.http.get(this.dashboardNetSales, { params: { time_frame: params } });
    }

    getNetPurchasesByCategory(params: string): Observable<any> {
      return this.http.get(this.dashboardCategorySort, { params: { time_frame: params } });
    }

    getNetPurchasesByItem(params: string): Observable<any> {
      return this.http.get(this.dashboardItemSort, { params: { time_frame: params } });
    }
}
