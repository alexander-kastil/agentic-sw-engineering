import { Component, signal } from '@angular/core';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('angular-devops');
  greeting = environment.greeting;

  count = 0;

  increment() {
    this.count++;
    console.log(`Button clicked ${this.count} times`);
  }
}
