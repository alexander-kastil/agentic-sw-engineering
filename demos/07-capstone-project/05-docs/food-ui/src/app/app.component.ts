import { Component, effect, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { SideMenuComponent } from './shared/sidemenu/sidemenu.component';
import { FoodContainerComponent } from './food/food-container/food-container.component';
import { MatSidenavModule } from '@angular/material/sidenav';
import { NgStyle } from '@angular/common';
import { environment } from '../environments/environment';
import { SideMenuService } from './shared/sidemenu/sidemenu.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    HomeComponent,
    NavbarComponent,
    SideMenuComponent,
    FoodContainerComponent,
    MatSidenavModule,
    NgStyle
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  nav = inject(SideMenuService);
  title = environment.title;

  navPosition = this.nav.getSideNavPosition();
  navVisible = this.nav.getSideNavVisible();
  workbenchMargin = {};

  constructor() {
    effect(() => {
      this.workbenchMargin = this.navVisible() ? { 'margin-left': '0.5rem' } : {};
      console.log('Workbench margin:', this.workbenchMargin);
    })
  }
}
