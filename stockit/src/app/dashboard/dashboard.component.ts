import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  profile: any;

  constructor(private dataService: MyDataService) { }
  
  ngOnInit(): void {
    this.dataService.getUserProfile().subscribe(data => {
      this.profile = data;
    });
  }

}
