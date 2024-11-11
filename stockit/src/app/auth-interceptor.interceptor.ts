import { HttpInterceptorFn } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { AuthService } from './auth.service';

export const authInterceptorInterceptor: HttpInterceptorFn = (req, next) => {
  
  const token = inject(AuthService).getToken();
  if (token) {
    const authReq = req.clone({
      setHeaders: {
        Authorization: `Token ${token}`
      }
    });
    return next(authReq);
  }
  
  return next(req);
};
