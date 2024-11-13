import { Component, OnInit, NgModule } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
import { error } from 'console';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { NgxChartsModule } from '@swimlane/ngx-charts';

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
 showModal: boolean = false;  // Flag to show/hide modal
 selectedItem: any = {};  // Holds the selected inventory item

 //form values
 newItem={
  name:'',
  cost: '',
  price: '',
  quantity:'',
  category:'',
  forecast_level:'',
 };

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
 }

 apiInventory(): void{
  this.myDataService.getInventory().subscribe(
    (data) => {
      //console to see items.______
      //console.log('got inventory data', data);
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

updateForecastingPreferences(): void {
  const url = `your-api-url/forecasting-preferences/${this.selectedItem.inventory_id}/`;  // Replace with your actual URL
  const data = {
    reorder_point: this.selectedItem.reorder_point,
    reorder_quantity: this.selectedItem.reorder_quantity
  };

  this.http.put(url, data).subscribe(
    (response) => {
      console.log('Updated successfully', response);
      this.showModal = false;  // Close the modal after successful update
      // You might want to update the inventoryList to reflect changes in the UI
    },
    (error) => {
      console.error('Error updating', error);
    }
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
