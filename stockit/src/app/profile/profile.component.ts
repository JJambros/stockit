import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {
  profile: any = {};
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getData().subscribe(
      (data) => (this.profile = data),
      (error) => console.error('error fetching data', error)
    );
  }
}
