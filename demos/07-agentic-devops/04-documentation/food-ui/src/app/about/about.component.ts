import { JsonPipe } from '@angular/common';
import { Component, ChangeDetectionStrategy } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { environment } from '../../environments/environment';

@Component({
    selector: 'app-about',
    imports: [MatCardModule, JsonPipe],
    templateUrl: './about.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './about.component.scss'
})
export class AboutComponent {
  config = environment;

}
