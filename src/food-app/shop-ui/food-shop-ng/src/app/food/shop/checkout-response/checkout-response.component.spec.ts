import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckoutResponseComponent } from './checkout-response.component';
import { AILoggerService } from '../../../logger/ai-logger.service';

describe('CheckoutResponseComponent', () => {
  let component: CheckoutResponseComponent;
  let fixture: ComponentFixture<CheckoutResponseComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [CheckoutResponseComponent],
      providers: [{ provide: AILoggerService, useValue: { logEvent: () => {} } }]
    });
    fixture = TestBed.createComponent(CheckoutResponseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
