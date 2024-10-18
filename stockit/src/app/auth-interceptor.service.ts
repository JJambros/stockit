import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable()
export class AuthInterceptorService implements HttpInterceptor {

  constructor(private authService: AuthService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the token from the auth service
    const token = this.authService.getToken();

    // Clone the request and add the Authorization header if the token exists
    if (token) {
      const authReq = req.clone({
        setHeaders: {
          Authorization: `Token ${token}`
        }
      });
      return next.handle(authReq);
    }

    // Pass on the original request if no token is available
    return next.handle(req);
  }
}
