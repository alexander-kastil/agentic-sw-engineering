import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { FoodItem } from './food.model';

@Injectable({
  providedIn: 'root'
})
export class FoodService {
  http = inject(HttpClient);

  getFood(): Observable<FoodItem[]> {
    return this.http.get<FoodItem[]>("/assets/food.json");
  }
}
