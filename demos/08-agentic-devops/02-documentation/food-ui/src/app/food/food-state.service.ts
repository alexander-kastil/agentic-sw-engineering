import { Injectable, computed, inject, signal } from '@angular/core';
import { FoodItem } from './food.model';
import { FoodService } from './food.service';

@Injectable({
  providedIn: 'root'
})
export class FoodStateService {
  service = inject(FoodService);
  #food = signal<FoodItem[]>([]);
  nextId = computed(() => {
    const food = this.#food();
    return food.length > 0 ? Math.max(...food.map((f) => f.id)) + 1 : 1;
  });

  constructor() {
    this.service.getFood().subscribe((data) => {
      this.#food.set(data);
    });
  }

  getFood() {
    return computed(() => this.#food());
  }

  getFoodById(id: number) {
    return computed(() => this.#food().find((f) => f.id === id));
  }

  addFood(food: FoodItem) {
    food.id = this.nextId();
    this.service.addFood(food).subscribe((data) => {
      this.#food.update((foods) => [...foods, data]);
    });
  }

  updateFood(food: FoodItem) {
    this.service.updateFood(food).subscribe((data) => {
      this.#food.update((foods) => {
        const index = foods.findIndex((f) => f.id === data.id);
        foods[index] = data;
        return foods;
      });
    });
  }

  deleteFood(id: number) {
    this.service.deleteFood(id).subscribe(() => {
      this.#food.update((foods) => foods.filter((f) => f.id !== id));
    });
  }
}
