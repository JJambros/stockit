import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {
  profile: any = {};
  constructor(private dataService: MyDataService, private authService: AuthService, private router: Router){}

  ngOnInit(): void {
    this.dataService.getUserProfile().subscribe(data => {
      this.profile = data;
    });
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        localStorage.removeItem('token');
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Logout failed:', error);
      }
    });
  }

}
