import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { NavItem } from './nav-item.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NavbarService {
  http = inject(HttpClient);

  getItems() {
    return this.http.get<NavItem[]>(environment.apiUrl + "menu-items");
  }
}
