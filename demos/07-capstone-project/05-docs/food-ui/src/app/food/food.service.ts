import { HttpClient } from "@angular/common/http";
import { Injectable, inject } from "@angular/core";
import { environment } from "../../environments/environment";
import { FoodItem } from "./food.model";

@Injectable({
  providedIn: "root",
})
export class FoodService {
  http = inject(HttpClient);
  private url = `${environment.apiUrl}food`;

  getFood() {
    return this.http.get<FoodItem[]>(this.url);
  }

  addFood(food: FoodItem) {
    return this.http.post<FoodItem>(this.url, food);
  }

  updateFood(food: FoodItem) {
    return this.http.put<FoodItem>(`${this.url}/${food.id}`, food);
  }

  deleteFood(id: number) {
    return this.http.delete<FoodItem>(`${this.url}/${id}`);
  }
}