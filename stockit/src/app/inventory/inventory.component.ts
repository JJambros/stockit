import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
import { error } from 'console';
@Component({
  selector: 'app-inventory',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inventory.component.html',
  styleUrls: ['./inventory.component.css'],
  providers: [MyDataService]
})
export class InventoryComponent implements OnInit  {
 inventoryList: any[] =[];

 constructor(private myDataService: MyDataService){}

 ngOnInit(): void {
   this.myDataService.getInventory().subscribe(
    (data) => {
      console.log('got inventory data', data);
      this.inventoryList = Array.isArray(data) ? data : [];
    },
    (error) => console.error('error fetching INVENTORY data', error)
   );
 }
}
