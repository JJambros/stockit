import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://localhost:8000';  // Django API URL

  constructor(private http: HttpClient) { }

  // Login method: Sends the username and password to Django
  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/login/`, { username, password });
  }

  // Logout method: Removes the token from Django and client storage
  logout(): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Token ${this.getToken()}`
    });
    return this.http.post(`${this.apiUrl}/api/logout/`, {}, { headers });
  }

  // Save the token to localStorage after login
  saveToken(token: string): void {
    localStorage.setItem('token', token);
  }

  // Get the token from localStorage
  getToken(): string | null {
    return localStorage.getItem('token');
  }

  // Remove the token from localStorage on logout
  removeToken(): void {
    localStorage.removeItem('token');
  }  
}
