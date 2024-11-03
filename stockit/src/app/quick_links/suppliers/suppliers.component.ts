import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../../my-data.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-suppliers',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './suppliers.component.html',
  styleUrl: './suppliers.component.css',
  providers: [MyDataService]
})
export class SuppliersComponent implements OnInit {
suppliersList: any[] =[];
constructor(private myDataService: MyDataService){}
ngOnInit(): void {
  this.myDataService.getSuppliers().subscribe(
    (data) => {
      console.log('got data', data);
      this.suppliersList = Array.isArray(data) ? data : [];
    }, 
    (error) => console.error('error fetching data', error)
  );
}
}
