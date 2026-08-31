import { Component, EventEmitter, Output, effect, inject, input } from '@angular/core';
import { FormGroup, NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormField } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FoodItem } from '../food.model';

@Component({
  selector: 'app-food-edit',
  standalone: true,
  imports: [ReactiveFormsModule, MatCardModule, MatFormField, MatButtonModule, MatInputModule],
  templateUrl: './food-edit.component.html',
  styleUrl: './food-edit.component.scss'
})
export class FoodEditComponent {
  food = input.required<FoodItem>();
  @Output() onFoodSave: EventEmitter<FoodItem> = new EventEmitter<FoodItem>();
  @Output() onCancelEdit: EventEmitter<void> = new EventEmitter<void>();
  fb = inject(NonNullableFormBuilder);

  form: FormGroup = this.fb.group({
    id: 0,
    name: ["", [Validators.required, Validators.minLength(3)]],
    price: [0, [Validators.required, Validators.min(1)]],
    items: [0, Validators.min(0)]
  });

  constructor() {
    effect(() => {
      console.log('Receiving data on input signal:', this.food());
      this.form.patchValue(this.food());
    });
  }

  saveFood(form: FormGroup) {
    if (this.food()) this.onFoodSave.emit(form.value);
  }

  cancelEdit() {
    this.onCancelEdit.emit();
  }
}