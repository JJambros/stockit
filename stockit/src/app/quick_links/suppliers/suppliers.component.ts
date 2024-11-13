import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../../my-data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-suppliers',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './suppliers.component.html',
  styleUrl: './suppliers.component.css',
  providers: [MyDataService]
})
export class SuppliersComponent implements OnInit {
suppliersList: any[] =[];
showSupplierForm = false;
newSupplier={
  supplier_name: '',
  contact_email: '',
  contact_phone: ''
};
constructor(private myDataService: MyDataService){}
ngOnInit(): void {
  this.myDataService.getSuppliers().subscribe(
    (data) => {
      //test display console
      // console.log('got suppliers data', data);
      this.suppliersList = Array.isArray(data) ? data : [];
    }, 
    (error) => console.error('error fetching supplier data', error)
  );
}

addSupplier(): void{
  this.myDataService.addSupplier(this.newSupplier).subscribe(
    (response) => {
      //check for console 
      // console.log('added supplier' , response);
      this.suppliersList.push(response);
      //reset and invis form 
      this.resetForm();
    },
    (error) => {
      console.error('Error adding supplier', error);
    }
  );
}

resetForm(): void{
  this.newSupplier = {
    supplier_name: '',
    contact_email: '',
    contact_phone: ''
  };
  this.showSupplierForm = false;
}

}
