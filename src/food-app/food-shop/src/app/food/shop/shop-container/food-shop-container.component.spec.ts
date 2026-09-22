import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideEntityData, withEffects } from '@ngrx/data';

import { FoodShopContainerComponent } from './food-shop-container.component';
import { cartFeature } from '../../state/cart/cart.state';
import { entityMetadata } from '../../state/catalog/entity-metadata';

describe('FoodShopContainerComponent', () => {
  let component: FoodShopContainerComponent;
  let fixture: ComponentFixture<FoodShopContainerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FoodShopContainerComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideStore({ [cartFeature.name]: cartFeature.reducer }),
        provideEffects(),
        provideEntityData({ entityMetadata }, withEffects()),
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(FoodShopContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
