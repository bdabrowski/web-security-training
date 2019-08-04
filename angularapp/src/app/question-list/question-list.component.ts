import {Component, OnInit} from '@angular/core';

import {QuestionService} from "../question.service";
import {FormBuilder} from "@angular/forms";
import {AuthService} from "../auth.service";


// Back-porting legacy elements of the app
declare function showSearchText(): any;

@Component({
  selector: 'app-question-list',
  templateUrl: './question-list.component.html',
})
export class QuestionListComponent implements OnInit {
  questions;
  newForm;
  searchForm;

  ngOnInit() {

  }

  constructor(
    private questionService: QuestionService,
    private formBuilder: FormBuilder,
  ) {

    this.newForm = this.formBuilder.group({
      subject: '',
      body: ''
    });
    this.searchForm = this.formBuilder.group({
      search: '',
    });
    this.questionService.getItems().subscribe((data) => this.questions = data);
  }

  onSubmit(data) {
    this.questionService.addItem(data).subscribe((responseData) => this.questions.push(data));
    this.newForm.reset();
  }

  onSearch(data) {
    this.questionService.getSearch(data).subscribe((data) => this.questions = data);
    showSearchText();
    this.newForm.reset();
  }

}
