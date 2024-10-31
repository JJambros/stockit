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

 edit(item: any): void{

  const newQuantity = prompt(`Enter new quantity for "${item.name}": `, item.quantity.toString());

  if(newQuantity === null){
    return;
  }

  const quantity_parsed = parseInt(newQuantity, 10);

  if(isNaN(quantity_parsed) || quantity_parsed < 0){
    alert('Cannot allow quantity go below 0');
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
