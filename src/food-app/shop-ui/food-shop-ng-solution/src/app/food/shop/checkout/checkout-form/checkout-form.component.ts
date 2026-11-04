
import { Component, EventEmitter, Input, Output, SimpleChanges, inject, signal } from '@angular/core';
import { FormArray, FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatToolbarModule } from '@angular/material/toolbar';
import { of } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { CustomersService } from '../../customers/customers.service';
import { EuroPipe } from '../../../../shared/euro.pipe';
import { BorderDirective, ColumnDirective } from '../../../formatting-directives';
import { CartItem } from '../../cart-item.model';
import { Order } from '../../order/order.model';

@Component({
  selector: 'app-checkout-form',
  templateUrl: './checkout-form.component.html',
  styleUrls: ['./checkout-form.component.scss'],
  standalone: true,
  imports: [MatToolbarModule, ReactiveFormsModule, BorderDirective, ColumnDirective, MatFormFieldModule, MatInputModule, MatButtonModule, MatSlideToggleModule, EuroPipe]
})
export class CheckoutFormComponent {
  @Input({ required: true }) order: Order = new Order();
  @Output() onCheckout = new EventEmitter<Order>();

  saveData = signal(false);

  fb = inject(FormBuilder);
  customersService = inject(CustomersService);
  orderForm = this.fb.group(
    {
      customer: this.fb.group({
        id: [{ value: this.order.customer.id }, { validators: [Validators.required] }],
        name: [this.order.customer.name, { validators: [Validators.required] }],
        email: [
          this.order.customer.email,
          { validators: [Validators.email, Validators.required] },
        ],
        phone: [this.order.customer.phone, { validators: [Validators.required] }],
      }),
      shippingAddress: this.fb.group({
        street: [this.order.shippingAddress.street, { validators: [Validators.required] }],
        city: [this.order.shippingAddress.city, { validators: [Validators.required] }],
        country: [this.order.shippingAddress.country, { validators: [Validators.required] }],
        zipCode: [this.order.shippingAddress.zipCode, { validators: [Validators.required] }],
      }),
      payment: this.fb.group({
        type: [this.order.payment.type, { validators: [Validators.required] }],
        accountNumber: [this.order.payment.accountNumber, { validators: [Validators.required] }]
      }),
      items: this.fb.array([]),
    });

  createOrderItems(items: CartItem[]) {
    let orderItems = this.orderForm.get('items') as FormArray;
    items.forEach(item => {
      orderItems.push(this.fb.group({
        itemId: [{ value: item.id, disabled: true }, { validators: [Validators.required] }],
        itemName: [{ value: item.name, disabled: true }, { validators: [Validators.required] }],
        itemPrice: [{ value: item.price, disabled: true }, { validators: [Validators.required] }],
        itemQuantity: [{ value: item.quantity, disabled: true }, { validators: [Validators.required] }],
      }));
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['order']) {
      this.orderForm.patchValue(changes['order'].currentValue);
      this.createOrderItems(this.order.items);
    }
  }

  completeCheckout() {
    const o = Object.assign({ ...this.order }, this.orderForm.value, { items: [...this.order.items] });
    if (!this.saveData()) {
      this.onCheckout.emit(o);
      return;
    }
    const customer = this.orderForm.get('customer')!.value as any;
    const address = this.orderForm.get('shippingAddress')!.value as any;
    this.customersService
      .saveCustomer({
        name: customer.name,
        email: customer.email,
        phone: customer.phone,
        street: address.street,
        city: address.city,
        country: address.country,
        zipCode: address.zipCode,
      })
      .pipe(switchMap(() => of(o)))
      .subscribe(order => this.onCheckout.emit(order));
  }
}
