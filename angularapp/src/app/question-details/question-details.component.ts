import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import {QuestionService} from "../question.service";
import {FormBuilder} from "@angular/forms";
import {AuthService} from "../auth.service";

@Component({
  selector: 'app-question-details',
  templateUrl: './question-details.component.html',
})
export class QuestionDetailsComponent implements OnInit {
  question;
  newAnswer;

  constructor(
    private route: ActivatedRoute,
    private questionService: QuestionService,
    private formBuilder: FormBuilder,
  ) {
    this.newAnswer = this.formBuilder.group({
      body: ''
    });

  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.questionService.getItem(params['questionId']).subscribe((data) => this.question = data);

    });
  }

  onSubmit(data) {
    data['question_id'] = this.question.id;
    this.questionService.addAnswer(data).subscribe((data) => this.questionService.getItem(data['question_id']).subscribe((data) => this.question = data));
    this.newAnswer.reset();
  }


}
