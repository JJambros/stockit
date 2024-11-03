import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../../my-data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-orders-summay',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './orders-summay.component.html',
  styleUrls: ['./orders-summay.component.css'],
  providers: [MyDataService]
})
export class OrdersSummayComponent implements OnInit {
  searchText='';
  orderSummary: any[] =[];
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getOrderSummary().subscribe(
      (data) => {
        console.log('got data', data);
         this.orderSummary = Array.isArray(data) ? data : [];
      },
      (error) => console.error('error fetching order summay data', error)
    );
  }


}
