import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { error } from 'console';

@Component({
  selector: 'app-audit',
  standalone: true,
  imports: [],
  templateUrl: './audit.component.html',
  styleUrl: './audit.component.css'
})
export class AuditComponent implements OnInit {
  auditTrails: any[] =[]; 
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getData().subscribe(
      (data) => (this.auditTrails = data),
      (error) => console.error('error fetching data', error)
    );
  }
}
