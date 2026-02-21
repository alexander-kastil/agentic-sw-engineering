import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FoodContainerComponent } from './food-container.component';

describe('FoodContainerComponent', () => {
  let component: FoodContainerComponent;
  let fixture: ComponentFixture<FoodContainerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FoodContainerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FoodContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
