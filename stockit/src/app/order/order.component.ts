import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-order',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.css']
})
export class OrderComponent implements OnInit {
  orders: any[] =[];
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getOrders().subscribe(
      (data) => {
        console.log('got data', data);
        this.orders = Array.isArray(data) ? data : [];
      }, 
      (error) => console.error('error fetching data', error)
    );
  }

  markAsShipped(orderId: number): void {
    this.myDataService.markOrderAsShipped(orderId).subscribe(
      (response) => {
        console.log('Order marked as shipped', response);
        // Optionally, update the order status here
      },
      (error) => {
        console.error('Error marking order as shipped', error);
      }
    );
  }
}
