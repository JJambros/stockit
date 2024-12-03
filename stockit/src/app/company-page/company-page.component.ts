import { Component, OnInit } from '@angular/core';
import { MyDataService } from '../my-data.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { error } from 'console';
@Component({
  selector: 'app-company-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './company-page.component.html',
  styleUrls: ['./company-page.component.css'],
  providers:[MyDataService],
})
export class CompanyPageComponent implements OnInit{
  //userList: any[] =[];

  newUser={
    username:'',
    password:'',
  };

  constructor(private myDataService: MyDataService){}
ngOnInit(): void {
}

addUser(): void{
  console.log('new:', this.newUser);
  this.myDataService.addUsers(this.newUser).subscribe(()=>{
     this.newUser={username:'',password:''};
    alert('user created sucessfully');
  },(error)=>{
    console.error('error adding new user',error);
  });
}


}
