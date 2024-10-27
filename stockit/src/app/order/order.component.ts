import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-order',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './order.component.html',
  styleUrl: './order.component.css'
})
export class OrderComponent implements OnInit {
  orders: any[] =[];
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getData().subscribe(
      (data) => (this.orders = data),
      (error) => console.error('error fetching data', error)
    );
  }
}
