import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  ChangeDetectionStrategy
} from '@angular/core';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { CatalogItem } from '../../catalog-item.model';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { EuroPipe } from '../../../shared/euro.pipe';

@Component({
    selector: 'app-food-list',
    templateUrl: './food-list.component.html',
    styleUrls: ['./food-list.component.scss'],
    standalone: true,
    changeDetection: ChangeDetectionStrategy.Eager,
    imports: [
        MatButtonModule,
        MatTableModule,
        MatIconModule,
        MatTooltipModule,
        EuroPipe,
    ],
})
export class FoodListComponent implements OnChanges {
  @Input() food: CatalogItem[] | null = [];
  @Input() selected: CatalogItem | null = null;
  @Output() foodSelected: EventEmitter<CatalogItem> =
    new EventEmitter<CatalogItem>();
  @Output()
  foodDeleted: EventEmitter<CatalogItem> = new EventEmitter<CatalogItem>();
  @Output()
  foodAdding: EventEmitter<CatalogItem> = new EventEmitter<CatalogItem>();
  displayedColumns: string[] = [
    'id',
    'name',
    'price',
    'instock',
    'editItem',
    'deleteItem',
  ];
  dataSource = new MatTableDataSource([]);

  ngOnChanges(changes: SimpleChanges) {
    if (changes['food']) {
      this.dataSource = new MatTableDataSource(changes['food'].currentValue);
    }
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  selectFood(p: CatalogItem) {
    this.foodSelected.emit(p);
  }

  deleteFood(item: CatalogItem) {
    this.foodDeleted.emit(item);
  }

  addFood() {
    this.foodAdding.emit(new CatalogItem());
  }
}
