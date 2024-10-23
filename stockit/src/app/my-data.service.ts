import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MyDataService {
  private apiUrl = 'http://localhost:8000/api/data/';  // Django API URL
  private profileUrl = 'http://localhost:8000/api/profile/';

  constructor(private http: HttpClient) { }

    getData(): Observable<any> {
      return this.http.get(this.apiUrl);
    } 

    getUserProfile(): Observable<any> {
      return this.http.get(this.profileUrl);
    }
}
