import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
// import { HttpClientModule } from '@angular/common/http';
@Component({
  selector: 'app-audit',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './audit.component.html',
  styleUrls: ['./audit.component.css'],
  providers: [MyDataService]
})
export class AuditComponent implements OnInit {
   auditTrails: any[] =[];
  constructor(private myDataService: MyDataService){}

  ngOnInit(): void {
    this.myDataService.getAudit().subscribe(
      (data) => {
        //console data vals
       // console.log('got data', data);
         this.auditTrails = Array.isArray(data) ? data.sort((a:any,b:any) => {
          const dateTimeA = new Date(`${a.formatted_date}T${a.formatted_time}`).getTime();
          const dateTimeB = new Date(`${b.formatted_date}T${b.formatted_time}`).getTime();
          return dateTimeB - dateTimeA;  // Descending order
        }) : [];
      },
      (error) => console.error('error fetching AUDIT data', error)
    );
  }
}
