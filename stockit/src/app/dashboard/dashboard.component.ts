import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';

interface RowData {
  type: string;
  amount: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  currentTime: Date = new Date();
  profile: any;
  orders: any;
  sales: any;
  breakdownData: any;
  errorMessage: string | null = null;

  constructor(private dataService: MyDataService) { }
  
  rowsByCategory: RowData[] = [];
  rowsByItem: RowData[] = [];

  rowsPerPage: number = 5;
  currentPageCategory: number = 1;
  currentPageItem: number = 1;

  paginatedRowsByCategory: RowData[] = [];
  paginatedRowsByItem: RowData[] = [];
  
  totalPagesCategory: number = 0;
  totalPagesItem: number = 0;

  totalPagesArrayCategory: number[] = [];
  totalPagesArrayItem: number[] = [];

  ngOnInit(): void {
    this.dataService.getUserProfile().subscribe(data => {
      this.profile = data;
    });

    this.dataService.getDashboardOrders('24h').subscribe(data => {
      this.orders = data;
    });

    this.dataService.getDashboardNetSales('24h').subscribe(data => {
      this.sales = data;
    });

    this.fetchDataByCategory();
    this.fetchDataByItem();
    this.fetchBreakdownData();
  }

  fetchBreakdownData(): void {
    this.dataService.getBreakdown().subscribe({
      next: (data) => {
        this.breakdownData = data;
        this.errorMessage = null;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = 'Could not load breakdown data';
      }
    });
  }

  fetchDataByCategory(timeFrame: string = '24h'): void {
    this.dataService.getNetPurchasesByCategory(timeFrame).subscribe(response => {
      this.rowsByCategory = response.net_purchases_by_category.map((item: any) => ({
        type: item['inventory__category__name'],
        amount: item.net_purchase.toFixed(2)  // Format as needed
      }));
      this.calculatePaginationByCategory();
    }, error => {
      console.error("Error fetching data:", error);
    });
  }

  fetchDataByItem(timeFrame: string = '24h'): void {
    this.dataService.getNetPurchasesByItem(timeFrame).subscribe(response => {
      this.rowsByItem = response.net_purchases_by_item.map((item: any) => ({
        type: item['inventory__name'],
        amount: item.net_purchase.toFixed(2)
      }));
      this.calculatePaginationByItem();
    }, error => {
      console.error("Error fetching data:", error);
    });
  }

  calculatePaginationByCategory(): void {
    this.totalPagesCategory = Math.ceil(this.rowsByCategory.length / this.rowsPerPage);
    this.totalPagesArrayCategory = Array.from({ length: this.totalPagesCategory }, (_, i) => i + 1);
    this.updatePaginatedRowsByCategory();
  }

  calculatePaginationByItem(): void {
    this.totalPagesItem = Math.ceil(this.rowsByItem.length / this.rowsPerPage);
    this.totalPagesArrayItem = Array.from({ length: this.totalPagesItem }, (_, i) => i + 1);
    this.updatePaginatedRowsByItem();
  }

  updatePaginatedRowsByCategory(): void {
    const start = (this.currentPageCategory - 1) * this.rowsPerPage;
    const end = start + this.rowsPerPage;
    this.paginatedRowsByCategory = this.rowsByCategory.slice(start, end);
  }

  updatePaginatedRowsByItem(): void {
    const start = (this.currentPageItem - 1) * this.rowsPerPage;
    const end = start + this.rowsPerPage;
    this.paginatedRowsByItem = this.rowsByItem.slice(start, end);
  }

  changePageCategory(page: number): void {
    if (page < 1 || page > this.totalPagesCategory) return;
    this.currentPageCategory = page;
    this.updatePaginatedRowsByCategory();
  }

  changePageItem(page: number): void {
    if (page < 1 || page > this.totalPagesItem) return;
    this.currentPageItem = page;
    this.updatePaginatedRowsByItem();
  }

}
