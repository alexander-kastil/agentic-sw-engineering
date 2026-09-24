import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { AILoggerService } from 'src/app/logger/ai-logger.service';
import { environment } from '../../../../environments/environment';
import { Order } from './order.model';

@Injectable({
  providedIn: 'root'
})
export class OrdersService {
  http = inject(HttpClient);
  logger = inject(AILoggerService);

  checkout(order: Order) {
    this.logger.logEvent('checking out order', order);
    var url = `${environment.ordersApi}/orders`;
    this.logger.logEventObject('using url', url);
    return this.http.post<Order>(`${environment.ordersApi}/orders`, order);
  }
}
