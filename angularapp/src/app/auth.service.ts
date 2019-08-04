import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";

@Injectable()
export class AuthService {

  constructor(private http: HttpClient) { }

    isSessionValid() {
      return this.http.get('http://localhost:8080/api/v1/auth/session')
    }

    logout() {
      return this.http.get('http://localhost:8080/api/v1/auth/logout')
    }
}
