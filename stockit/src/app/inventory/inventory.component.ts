

import { Component, OnInit, NgModule } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
import { error } from 'console';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { data } from 'jquery';

interface PieChartData {
  name: string;
  value: number;
}

@Component({
  selector: 'app-inventory',
  standalone: true,
  imports: [CommonModule, FormsModule, NgxChartsModule],
  templateUrl: './inventory.component.html',
  styleUrls: ['./inventory.component.css'],
  providers: [MyDataService]
})
export class InventoryComponent implements OnInit  {
 inventoryList: any[] =[];
 categories: any[] =[];
 showInvenoryForm: boolean = false; //default doesn't display form
//  showCategoryForm: boolean = false;
 showModal: boolean = false;  // Flag to show/hide modal
 selectedItem: any = {};  // Holds the selected inventory item

 //form values
 newItem={
  name:'',
  cost: '',
  price: '',
  quantity:'',
  forecast_level:'',
  category: '',
 };

//  newCategory={
//   name:'',
//   description:'',
//  };

 // Pie chart options
 single: any[] = [];
 view: any[] = [700, 400];

 // options
 gradient: boolean = true;
 showLegend: boolean = true;
 showLabels: boolean = true;
 isDoughnut: boolean = false;
 legendPosition: string = 'below';

 colorScheme = {
   domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
 };

 constructor(private myDataService: MyDataService){}

 ngOnInit(): void {
  this.apiInventory();
  this.apiCategories();
 }

 apiInventory(): void{
  this.myDataService.getInventory().subscribe(
    (data) => {
      //console to see items.______
      // console.log('got inventory data', data);
      this.inventoryList = Array.isArray(data) ? data : [];
      this.transformDataForChart();
    },
    (error) => console.error('error fetching INVENTORY data', error)
   );
 }

 // Pie chart methods
 transformDataForChart(): void {
  // Transform the inventory data into the format required by the pie chart
  this.single = this.inventoryList.map(item => ({
    name: item.category.name, // Assuming category object has a 'name' field
    value: item.quantity
  }));
}

onSelect(data: PieChartData): void {
  console.log('Item clicked', JSON.parse(JSON.stringify(data)));
}

onActivate(data: PieChartData): void {
  console.log('Activate', JSON.parse(JSON.stringify(data)));
}

onDeactivate(data: PieChartData): void {
  console.log('Deactivate', JSON.parse(JSON.stringify(data)));
}

// Modal methods
editAlert(item: any): void {
  this.selectedItem = { ...item };  // Make a copy of the item to avoid mutating the original
  this.showModal = true;  // Show the modal
}

closeModal(): void {
  this.showModal = false;
}




apiCategories():void{
  this.myDataService.getCategories().subscribe((data)=>{
    this.categories=Array.isArray(data) ? data :[];
  },(error)=>{
    console.error('error categories data',error);
  });
}
//add form
addInventory(): void{
  console.log('new:', this.newItem);
  this.myDataService.addInventoryItem(this.newItem).subscribe(()=>{
    this.apiInventory();
    this.showInvenoryForm = false;
    alert('item created sucessfully');
  },(error)=>{
    console.error('error adding new inventory',error);
  });
}

// addCategory(): void{
//   console.log('new category: ', this.newCategory);
//   this.myDataService.addCategories(this.newCategory).subscribe(()=>{
//     this.apiInventory();
//     this.showCategoryForm = false;
//     alert('category created sucessfully');
//   },(error)=>{
//     console.error('error adding new category',error);
//   });
// }

 updateItemQuantity(item: any){
  this.myDataService.updateInventoryItem(item).subscribe(
    (data) => {
      alert('Inventory quantity updated sucessfully ');
    },
    (error)=>{
      alert('Error updating Inventory Quantity');
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
