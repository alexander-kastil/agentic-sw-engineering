import { JsonPipe } from '@angular/common';
import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [MatCardModule, JsonPipe],
  templateUrl: './about.component.html',
  styleUrl: './about.component.scss'
})
export class AboutComponent {
  config = environment;

}
