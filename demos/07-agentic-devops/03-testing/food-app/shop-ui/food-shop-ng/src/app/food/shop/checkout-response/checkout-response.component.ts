import { Component, Input, SimpleChanges, inject, ChangeDetectionStrategy } from '@angular/core';

import { Order } from '../order/order.model';
import { MatCardModule } from '@angular/material/card';
import { AILoggerService } from 'src/app/logger/ai-logger.service';

@Component({
  selector: 'app-checkout-response',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './checkout-response.component.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrls: ['./checkout-response.component.scss']
})
export class CheckoutResponseComponent {
  @Input() response: Order | null = null;
  logger = inject(AILoggerService);

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['response']) {
      this.logger.logEvent('checkout response', changes['response'].currentValue);
    }
  }
}
