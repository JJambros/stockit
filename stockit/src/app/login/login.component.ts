import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) { }

  onLogin(): void {
    this.authService.login(this.username, this.password).subscribe(
      (response) => {
        // Save the token in localStorage
        this.authService.saveToken(response.token);

        // Navigate to protected landing page
        this.router.navigate(['/dashboard']);
      },
      (error) => {
        console.error('Login failed', error);
        alert('Invalid login credentials');
      }
    );
  }
}
