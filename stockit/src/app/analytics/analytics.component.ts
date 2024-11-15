import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analytics.component.html',
  styleUrl: './analytics.component.css'
})
export class AnalyticsComponent implements OnInit {
  inventoryForecastList: any[] = [];
  errorMessage: string | null = null;

  constructor(private dataService: MyDataService) { }

  ngOnInit(): void {
    this.loadInventoryForecastData();
  }

  loadInventoryForecastData(): void {
    this.dataService.getInventory().subscribe(
      (inventoryList) => {
        this.inventoryForecastList = [];

        // Loop through each inventory item and fetch forecast data
        inventoryList.forEach((item: any) => {
          this.dataService.getInventoryForecast(item.inventory_id, '2024-12-01').subscribe(
            (forecastData) => {
              // Store forecast data along with inventory item info
              this.inventoryForecastList.push({ ...item, ...forecastData });
            },
            (error) => console.error(`Error fetching forecast for inventory ${item.inventory_id}`, error)
          );
        });
      },
      (error) => {
        console.error('Error fetching inventory data', error);
        this.errorMessage = 'Could not load inventory data.';
      }
    );
  }
}

