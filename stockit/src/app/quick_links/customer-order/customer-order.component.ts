import { CommonModule } from '@angular/common';
import { Component , OnInit} from '@angular/core';
import { MyDataService } from '../../my-data.service';

@Component({
  selector: 'app-customer-order',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './customer-order.component.html',
  styleUrl: './customer-order.component.css',
  providers: [MyDataService]
})
export class CustomerOrderComponent implements OnInit {

  customerOrders: any[] =[];
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getCusomerOrder().subscribe(
      (data) => {
        console.log('got customer orders data', data);
         this.customerOrders = Array.isArray(data) ? data : [];
      },
      (error) => console.error('error fetching customer orders data', error)
    );
  }
}
