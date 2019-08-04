import {Component, OnInit} from '@angular/core';
import {AuthService} from "./auth.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit  {

  constructor(private authService: AuthService) {}

  onLogout() {
    this.authService.logout().subscribe((data) => window.location.href = 'http://localhost:8080/auth/login');
  }

  ngOnInit() {
    this.authService.isSessionValid().subscribe((data) => {
      if(data['user_id']) {
        console.log('user session active')
      } else {
        console.log('user session inactive login redirect');
        window.location.href = 'http://localhost:8080/auth/login'
      }
    });
  }

}
