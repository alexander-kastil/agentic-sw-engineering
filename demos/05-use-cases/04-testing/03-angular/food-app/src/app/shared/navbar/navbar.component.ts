import { Component, inject } from '@angular/core';
import { NavbarService } from './navbar.service';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {
  ns = inject(NavbarService);
  navItems = toSignal(this.ns.getItems());


}
