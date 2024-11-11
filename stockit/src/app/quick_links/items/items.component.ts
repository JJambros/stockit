import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../../my-data.service';

@Component({
  selector: 'app-items',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './items.component.html',
  styleUrl: './items.component.css',
  providers: [MyDataService]
})
export class ItemsComponent implements OnInit {
  itemsList: any[]=[];
  constructor(private myDataService: MyDataService){}
ngOnInit(): void {
  this.myDataService.getInventory().subscribe(
    (data) => {
      console.log('got inventory data', data);
      this.itemsList = Array.isArray(data) ? data : [];
    }, 
    (error) => console.error('error fetching data', error)
  );
}
}
