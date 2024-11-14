import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../../my-data.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-items',
  standalone: true,
  imports: [CommonModule, FormsModule],
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

  deleteItem(id: number){
    if(confirm('Are you sure you want to delete this item from inventory?')){
      this.myDataService.softDeleteItems(id).subscribe(
      (data) => {
        console.log('deleted item', data);
        this.itemsList = this.itemsList.filter((item) => item.inventory_id !== id);
      },
      (error) => console.error('error deleting item', error)
    );
    }
  }

  updateItem(item: any) {
    if(confirm('Are you sure you want to update this item?')){
      this.myDataService.updateInventoryItem(item).subscribe(
      (data) => {
        console.log('Updated item:', data);
        // Optionally refresh the item in itemsList or display a success message
      },
      (error) => console.error('Error updating item:', error)
    );
    }
  }
}
