import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
import { error } from 'console';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-inventory',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './inventory.component.html',
  styleUrls: ['./inventory.component.css'],
  providers: [MyDataService]
})
export class InventoryComponent implements OnInit  {
 inventoryList: any[] =[];
 categories: any[] =[];
 showInvenoryForm: boolean = false; //default doesn't display form
 //form values
 newItem={
  name:'',
  cost: '',
  price: '',
  quantity:'',
  category:'',
  forecast_level:'',
 };
 constructor(private myDataService: MyDataService){}

 ngOnInit(): void {
  this.apiInventory();
 }
 apiInventory(): void{
  this.myDataService.getInventory().subscribe(
    (data) => {
      //console to see items.______
      //console.log('got inventory data', data);
      this.inventoryList = Array.isArray(data) ? data : [];
    },
    (error) => console.error('error fetching INVENTORY data', error)
   );
 }

//  apiCategories(): void{
//   this.myDataService.getCategories().subscribe(
//     (data) => {
//       //console to see items.______
//       console.log('got categoies data', data);
//       this.categories = Array.isArray(data) ? data : [];
//     },
//     (error) => console.error('error fetching categories data', error)
//    );
//  }

//add form
addInventory(): void{
  //test print to console item added details
  console.log('item: ', this.newItem);
  this.myDataService.addInventoryItem(this.newItem).subscribe( () =>{
    this.apiInventory();
    this.showInvenoryForm = false;
  },
  (error) => console.error('error adding an item' , error)
  );
}
//quantity
 edit(item: any): void{

  item.editQ=true;
  item.newQuantity = item.quantity;

 }

 updateQuantity(item: any):void{
  const quantity_parsed = parseInt(item.newQuantity, 10);
  if(isNaN(quantity_parsed) || quantity_parsed < 0){
    alert('Please re-enter a non-negative number.');
    return;
  }

  const updatedItem = {...item, quantity: quantity_parsed};
  
  this.myDataService.updateInventoryItem(updatedItem).subscribe( () =>{
    //console check
    console.log(`${item.inventory_id} quantity updated`);
    this.apiInventory();
  },

  (error) => {
    console.error('error updating', error);
  }
);
 }

 cancelEdit(item:any):void{
  item.editQ =false;
 }


  

//   


 

 softDelete(itemId: number): void{
  if(confirm('Are you sure you want to delete this item from inventory?')){
    this.myDataService.softDeleteItems(itemId).subscribe( () =>{
      console.log('item SOFT-deleted');
      this.apiInventory();
    },
    (error) => console.error('error SOFT deleting', error)
    );
  }
 }
}
