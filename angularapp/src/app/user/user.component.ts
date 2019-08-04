import { Component, OnInit } from '@angular/core';
import {FormBuilder} from "@angular/forms";
import {UserService} from "../user.service";
import {AuthService} from "../auth.service";

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
})
export class UserComponent implements OnInit {
  updateForm;
  user;
  constructor(
    private userService: UserService,
    private formBuilder: FormBuilder,
  ) {

    this.updateForm = this.formBuilder.group({
      first_name: '',
      last_name: ''
    });

  }
  onSubmit(data) {
    this.userService.updateItem(data).subscribe( (data) => this.userService.getItem().subscribe((data) => {
      this.user = data;
      this.updateForm.controls['first_name'].patchValue(data['first_name']);
      this.updateForm.controls['last_name'].patchValue(data['last_name']);
    }));
    this.updateForm.reset();
  }

  ngOnInit() {
    this.userService.getItem().subscribe((data) => {
      this.user = data;
      this.updateForm.controls['first_name'].patchValue(data['first_name']);
      this.updateForm.controls['last_name'].patchValue(data['last_name']);

    })
  }

}
