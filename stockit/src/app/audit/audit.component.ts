import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-audit',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './audit.component.html',
  styleUrls: ['./audit.component.css'],
  providers: [MyDataService]
})
export class AuditComponent implements OnInit {
  // auditTrails: AuditTrail[] =[]; 
  auditTrails:any;
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getAudit().subscribe(
      (data) => {
        console.log('got data', data);
        this.auditTrails =data;
        // this.auditTrails = Array.isArray(data) ? data : [];
      },
      (error) => console.error('error fetching data', error)
    );
  }
}