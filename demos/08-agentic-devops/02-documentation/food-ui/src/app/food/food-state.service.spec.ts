import { TestBed } from '@angular/core/testing';

import { FoodStateService } from './food-state.service';

describe('FoodStateService', () => {
  let service: FoodStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FoodStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
