import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
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
  private orderItemsUrl = 'http://localhost:8000/api/order-items/';
  private customerOrderUrl = 'http://localhost:8000/api/customer-orders/';
  private suppliersUrl = 'http://localhost:8000/api/suppliers/';
  private categoriesUrl = 'http://localhost:8000/api/categories/';
  private dashboardBreakdown = 'http://localhost:8000/api/dashboard/total-breakdown/';
  private inventoryForecast = 'http://localhost:8000/api/inventory/forecast';
  //
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

    // Orders page
    getOrders(): Observable<any>{
      return this.http.get(this.orderUrl);
    }

    markOrderAsShipped(orderId: number): Observable<any> {
      return this.http.post<any>(`http://localhost:8000/api/orders/${orderId}/mark_shipped/`, {});
    }

    getCustomerOrders(): Observable<any> {
      return this.http.get('http://localhost:8000/api/customer-orders/');
    }

    getPurchaseOrders(): Observable<any> {
      return this.http.get('http://localhost:8000/api/purchase-orders/');
    }

    //inventory 
    getInventory(): Observable<any>{
      return this.http.get(this.inventoryUrl);
    }

    updateInventoryItem(item:any): Observable<any>{
      return this.http.put(`${this.inventoryUrl}${item.inventory_id}/`, item);
    }

    // getCategories(): Observable<any>{
    //   return this.http.get(this.categoriesUrl);
    // }
    addInventoryItem(item:any): Observable<any>{
      return this.http.post(this.inventoryUrl, item);
    }

    softDeleteItems(itemId: number): Observable<any>{
      return this.http.delete(`${this.inventoryUrl}${itemId}/`);
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

    getOrderSummary() :Observable<any>{
      return this.http.get(this.orderItemsUrl);
    }

    getCusomerOrder():Observable<any>{
      return this.http.get(this.customerOrderUrl);
    }

    getSuppliers():Observable<any>{
      return this.http.get(this.suppliersUrl);
    }

    addSupplier(supplier: any): Observable<any>{
      return this.http.post(this.suppliersUrl, supplier);
    }

    getBreakdown(timeFrame: string = 'overall', breakdownType: string = 'item'): Observable<any> {
      let params = new HttpParams()
        .set('time_frame', timeFrame)
        .set('breakdown_type', breakdownType);
  
      return this.http.get<any>(this.dashboardBreakdown, { params });
    }

    getInventoryForecast(inventoryId: number, forecastDate: string): Observable<any> {
      return this.http.get(`${this.inventoryForecast}/${inventoryId}/${forecastDate}/`);
    }

    addPurchaseOrder(payload: any): Observable<any> {
      return this.http.post('http://localhost:8000/api/purchase-orders/', payload);
    }

    addCustomerOrder(payload: any): Observable<any> {
      return this.http.post('http://localhost:8000/api/customer-orders/', payload);
    }

    getLocation(): Observable<any> {
      return this.http.get('http://localhost:8000/api/locations/');
    }

    getStatus(): Observable<any> {    
      return this.http.get('http://localhost:8000/api/order-status/');
    } 
}
