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

activeSupplier: any = {};
showEditForm=false;
editSupplier(supplier:any):void{
  this.activeSupplier = {...supplier };
  this.showEditForm = true;
}

updateSupplier():void{
  this.myDataService.updateSupplier(this.activeSupplier.supplier_id,
    this.activeSupplier).subscribe((response) => {
      //find where specific supplier is based on id to update
      const index = this.suppliersList.findIndex(s => s.supplier_id === response.supplier_id);
      //update
      if(index > -1) {
        this.suppliersList[index] = response;
      }
      this.showEditForm = false;
    },(error)=> {
      console.error('error updating supplier',error);
    }
  );
}

softDeleteSupplier(supplierId: number): void{
  const confirmSupplierDeletion = window.confirm('Are you sure you want to delete this suppllier?');
  if(confirmSupplierDeletion){
    this.myDataService.soft_deleteSupplier(supplierId).subscribe(
      (response) => {
        this.suppliersList = this.suppliersList.filter(s => s.supplier_id !== supplierId);
      },(error)=>{
        console.error('error SOFT deleting supplier', error);
      }
    );
  }else{
    // console.log('Delete action cancelled');
  }
  
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
