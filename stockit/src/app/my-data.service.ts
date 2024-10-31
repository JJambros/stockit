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
    //update inventory
    updateInventoryItem(item:any): Observable<any>{
      return this.http.put(`${this.inventoryUrl}${item.inventory_id}/`, item);
    }
    //delete invetory
    softDeleteItems(itemId: number): Observable<any>{
      return this.http.delete(`${this.inventoryUrl}${itemId}/`);
    }
}
