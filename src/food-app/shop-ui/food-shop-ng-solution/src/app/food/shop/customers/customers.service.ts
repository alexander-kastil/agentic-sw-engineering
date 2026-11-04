import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';

export interface CustomerDto {
  name: string;
  email: string;
  phone: string;
  street: string;
  city: string;
  country: string;
  zipCode: string;
}

@Injectable({
  providedIn: 'root',
})
export class CustomersService {
  private http = inject(HttpClient);

  saveCustomer(customer: CustomerDto): Observable<unknown> {
    return this.http.post<unknown>(`${environment.catalogApi}/api/customers`, customer);
  }
}
