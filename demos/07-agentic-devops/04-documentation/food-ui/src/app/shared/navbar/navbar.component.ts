import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { NavItem } from './nav-item.model';
import { NavbarService } from './navbar.service';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { SideMenuService } from '../sidemenu/sidemenu.service';
import { MatIconModule } from '@angular/material/icon';
import { AsyncPipe } from '@angular/common';

@Component({
    selector: 'app-navbar',
    imports: [RouterLink, RouterLinkActive, MatToolbarModule, MatIconModule, AsyncPipe],
    templateUrl: './navbar.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  nav = inject(NavbarService);
  navItems = this.nav.getItems()
  sideMenu = inject(SideMenuService);
  navVisible = this.sideMenu.getSideNavVisible();

  toggleMenu() {
    this.sideMenu.toggleMenuVisibility();
  }
}
