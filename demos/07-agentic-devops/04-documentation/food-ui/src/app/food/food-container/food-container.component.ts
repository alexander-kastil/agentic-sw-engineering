import { Component, inject } from '@angular/core';
import { FoodEditComponent } from '../food-edit/food-edit.component';
import { FoodListComponent } from '../food-list/food-list.component';
import { FoodStateService } from '../food-state.service';
import { FoodItem } from '../food.model';

@Component({
  selector: 'app-food-container',
  standalone: true,
  imports: [FoodListComponent, FoodEditComponent],
  templateUrl: './food-container.component.html',
  styleUrl: './food-container.component.scss'
})
export class FoodContainerComponent {
  fs = inject(FoodStateService);
  food = this.fs.getFood();
  selected: FoodItem | null = null;

  selectFood(food: FoodItem) {
    console.log('selecting', food);
    this.selected = { ...food };
  }

  deleteFood(food: FoodItem) {
    this.fs.deleteFood(food.id);
  }

  foodSaved(item: FoodItem) {
    if (item.id === 0) {
      this.fs.addFood(item);
    } else {
      this.fs.updateFood(item);
    }
    this.selected = null;
  }

  addFood() {
    this.selected = new FoodItem();
  }

  cancelEdit() {
    this.selected = null;
  }
}
