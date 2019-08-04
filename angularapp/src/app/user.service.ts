import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class UserService {
  getItem() {
    return this.http.get('http://localhost:8080/api/v1/forum/profile/');
  }

  updateItem(data) {
    return this.http.put('http://localhost:8080/api/v1/forum/profile/', data)
  }

  constructor(
    private http: HttpClient
  ) {}

}
