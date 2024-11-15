import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-order',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.css']
})
export class OrderComponent implements OnInit {
  customerOrders: any[] =[];
  purchaseOrders: any[] =[];
  inventoryItems: any[] = [];
  suppliers: any[] = [];
  activeTable: string = 'purchase';
  location: any[] = [];
  status: any[] = [];

  // Today's date for order date
  today: string = new Date().toISOString().split('T')[0];

  // New order data
  newOrder = {
    order_quantity: null,
    po_date: '',
    inventory: null,
    supplier: null
  };

  // New order data
  newCustomerOrder = {
    co_from: '',
    co_to: '',
    co_date: '',

  };

  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getCustomerOrders().subscribe(
      (data) => {
        console.log('got data', data);
        this.customerOrders = Array.isArray(data) ? data : [];
      }, 
      (error) => console.error('error fetching data', error)
    );

    this.myDataService.getPurchaseOrders().subscribe(
      (data) => {
        console.log('got data', data);
        this.purchaseOrders = Array.isArray(data) ? data : [];
      }, 
      (error) => console.error('error fetching data', error)
    );

    this.myDataService.getInventory().subscribe(
      (data: string[]) => {
        this.inventoryItems = data;
      },
      (error) => console.error('error fetching inventory items', error)
    );

    this.myDataService.getSuppliers().subscribe(
      (data: string[]) => {
        this.suppliers = data;
      },
      (error) => console.error('error fetching suppliers', error)
    );

    

    this.newOrder.po_date = this.today;
    this.newCustomerOrder.co_date = this.today;
  }

  markAsShipped(orderId: number): void {
    this.myDataService.markOrderAsShipped(orderId).subscribe(
      (response) => {
        console.log('Order marked as shipped', response);
        // Optionally, update the order status here
      },
      (error) => {
        console.error('Error marking order as shipped', error);
      }
    );
  }

  showTable(tableType: string) {
    this.activeTable = tableType;
  }

  addPurchaseOrder(): void {
  // Validate the input fields
  if (!this.newOrder.order_quantity || !this.newOrder.inventory || !this.newOrder.supplier) {
    alert('Please fill out all fields.');
    return;
  }

  // Prepare the payload to send to the backend
  const payload = {
    order_quantity: this.newOrder.order_quantity,
    po_date: this.newOrder.po_date,
    inventory: Number(this.newOrder.inventory),  // send the inventory ID
    supplier: Number(this.newOrder.supplier),     // send the supplier ID
  };

  // Call the service to add the purchase order
  this.myDataService.addPurchaseOrder(payload).subscribe(
    (response) => {
      console.log('Purchase order added successfully:', response);

      // Find inventory and supplier details to display in the table
      const inventoryDetails = this.inventoryItems.find(item => item.inventory_id === payload.inventory);
      const supplierDetails = this.suppliers.find(item => item.supplier_id === payload.supplier);

      // Add the new order with full details to the purchaseOrders array
      this.purchaseOrders.push({
        id: response.id, // Assuming the backend returns the new order's ID
        order_quantity: payload.order_quantity,
        po_date: payload.po_date,
        inventory: inventoryDetails ? inventoryDetails.name : 'Unknown', // Replace with the actual field name
        supplier: supplierDetails ? supplierDetails.supplier_name : 'Unknown',   // Replace with the actual field name
        is_deleted: false // Default value, update if needed
      });

      // Reset form fields
      this.newOrder = {
        order_quantity: null,
        po_date: this.today,
        inventory: null,
        supplier: null
      };
    },
    (error) => {
      console.error('Error adding purchase order:', error, 'Payload:', payload);
      alert('Failed to add purchase order. Please try again.');
    }
  );
}

}
