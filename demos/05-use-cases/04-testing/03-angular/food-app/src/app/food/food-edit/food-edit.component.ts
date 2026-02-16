import { Component, EventEmitter, Input, Output, SimpleChanges } from '@angular/core';
import { FoodItem } from '../food.model';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-food-edit',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './food-edit.component.html',
  styleUrl: './food-edit.component.scss'
})
export class FoodEditComponent {
  @Input({ required: true }) food: FoodItem = new FoodItem();
  @Output() onFoodSave: EventEmitter<FoodItem> = new EventEmitter<FoodItem>();

  ngOnChanges(changes: SimpleChanges): void {
    console.log("receiving data on input:", changes["food"]);
  }

  saveFood() {
    if (this.food) this.onFoodSave.emit(this.food);
  }
}