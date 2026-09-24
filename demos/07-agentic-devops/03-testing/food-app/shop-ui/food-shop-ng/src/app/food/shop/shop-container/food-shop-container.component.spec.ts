import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { CatalogItem } from '../../catalog-item.model';
import { CartFacade } from '../../state/cart/cart.facade';
import { FoodEntityService } from '../../state/catalog/food-entity.service';
import { FoodShopContainerComponent } from './food-shop-container.component';

describe('FoodShopContainerComponent', () => {
  let component: FoodShopContainerComponent;
  let fixture: ComponentFixture<FoodShopContainerComponent>;

  const food: CatalogItem[] = [{ id: 4, name: 'Falafel Plate', price: 12, inStock: 9 }];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FoodShopContainerComponent],
      providers: [
        { provide: FoodEntityService, useValue: { entities$: of(food), loaded$: of(true) } },
        { provide: CartFacade, useValue: { getItems: () => of([]), set: () => { } } },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(FoodShopContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('renders one shop item per catalog entity', () => {
    expect(fixture.nativeElement.querySelectorAll('app-shop-item').length).toBe(food.length);
  });
});
