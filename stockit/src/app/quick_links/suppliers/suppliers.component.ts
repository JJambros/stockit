import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../../my-data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { error } from 'console';

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


deleteSupplier(id: number): void{
  const confirmSupplierDeletion = window.confirm('Are you sure you want to delete this suppllier?');
  if(confirmSupplierDeletion){
    this.myDataService.softdeleteSupplier(id).subscribe(
      (data) => {
        this.suppliersList = this.suppliersList.filter((supplier) => supplier.supplier_id !== id);
      },(error)=>{
        console.error('error SOFT deleting supplier', error);
      }
    );
  }else{
   console.log('Delete action cancelled');
  }

}

updateSupplier(supplier:any){
  console.log('supplier id updated: ',supplier.supplier_id);
  this.myDataService.updatesSupplier(supplier).subscribe((data)=>{
    console.log('updated',data);
  },(error)=>{
    console.error('error updating supplier', error);
  });
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
