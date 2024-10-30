import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MyDataService } from '../../my-data.service';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.css'
})
export class MainLayoutComponent implements OnInit {
  profile: any;

  constructor(private dataService: MyDataService) { }

  ngOnInit(): void {
    this.dataService.getUserProfile().subscribe(data => {
      this.profile = data;
    });
  }

}
