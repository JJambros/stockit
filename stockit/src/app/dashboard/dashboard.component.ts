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
  orders: any;
  sales: any;

  constructor(private dataService: MyDataService) { }
  
  ngOnInit(): void {
    this.dataService.getUserProfile().subscribe(data => {
      this.profile = data;
    });

    this.dataService.getDashboardOrders('24h').subscribe(data => {
      this.orders = data;
    });

    this.dataService.getDashboardNetSales('24h').subscribe(data => {
      this.sales = data;
    });
  }

}
