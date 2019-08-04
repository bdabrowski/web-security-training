import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class QuestionService {

  getItems() {
    return this.http.get('http://localhost:8080/api/v1/forum/question/');
  }

  getSearch(q) {
    return this.http.get('http://localhost:8080/api/v1/forum/question/?q=' + q['search']);
  }

  getItem(id) {
    return this.http.get('http://localhost:8080/api/v1/forum/question/' + id)
  }

  addItem(data) {
    return this.http.post('http://localhost:8080/api/v1/forum/question/', data)
  }

  addAnswer(data) {
    return this.http.post('http://localhost:8080/api/v1/forum/answer/', data)
  }

  constructor(
    private http: HttpClient
  ) {}

}
