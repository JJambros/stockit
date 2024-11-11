import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MyDataService } from './my-data.service';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'stockit';
  message: string = '';
  
  constructor(private myDataService: MyDataService) {}

  ngOnInit(): void {
/*     this.myDataService.getData().subscribe(
      (data) => {
        this.message = data.message;
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    ); */
  }

}
