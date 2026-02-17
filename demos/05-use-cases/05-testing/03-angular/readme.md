# Angular Testing

Generate tests for the following components:

- nav-bar.service.spec.ts
- navbar.component.spec.ts
- food-list.component.spec.ts
- food-list.component.spec.ts

##  nav-bar.service.spec.ts

```typescript
describe('NavbarService', () => {
  let service: NavbarService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        NavbarService
      ]
    });

    service = TestBed.inject(NavbarService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should retrieve nav items from API via GET', () => {
    const dummyNavItems: NavItem[] = [
      { title: 'Home', url: '/home' },
      { title: 'About', url: '/about' }
    ];

    service.getItems().subscribe(navItems => {
      expect(navItems.length).toBe(2);
      expect(navItems).toEqual(dummyNavItems);
    });

    const request = httpMock.expectOne(`${environment.apiUrl}`);
    expect(request.request.method).toBe('GET');
    request.flush(dummyNavItems);
  });

  afterEach(() => {
    httpMock.verify();
  });
});
```

## navbar.component.spec.ts

```typescript
describe('NavbarComponent', () => {
  let component: NavbarComponent;
  let fixture: ComponentFixture<NavbarComponent>;
  let navbarServiceSpy: any;

  beforeEach(() => {
    navbarServiceSpy = jasmine.createSpyObj('NavbarService', ['getItems']);
    navbarServiceSpy.getItems.and.returnValue(
      of([{ title: 'Home', url: '/' }, { title: 'About', url: '/about' }])
    );

    fixture = TestBed.configureTestingModule({
      imports: [NavbarComponent],
      providers: [{ provide: NavbarService, useValue: navbarServiceSpy }]
    }).createComponent(NavbarComponent);

    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the nav item', () => {
    fixture.detectChanges();
    const navItems = fixture.nativeElement.querySelectorAll('.menuItem');
    expect(navItems.length).toBe(2);
    expect(navItems[0].textContent).toContain('Home');
    expect(navItems[1].textContent).toContain('About');
  });
});
```

## food-list.component.spec.ts

```typescript
it('should emit foodSelected event', () => {
    const item = { id: 1, name: 'Test', calories: 100, price: 10 };
    spyOn(component.foodSelected, 'emit');
    component.selectFood(item);
    expect(component.foodSelected.emit).toHaveBeenCalledWith(item);
    });

    it('should emit foodDeleted event', () => {
    const item = { id: 1, name: 'Test', calories: 100, price: 10 };
    spyOn(component.foodDeleted, 'emit');
    component.deleteFood(item);
    expect(component.foodDeleted.emit).toHaveBeenCalledWith(item);
});

it('should render food items', () => {
    const items = [
        { id: 1, name: 'Test 1', calories: 100, price: 10 },
        { id: 2, name: 'Test 2', calories: 200, price: 20 }
    ];
    component.food = items;
    fixture.detectChanges();
    const compiled = fixture.nativeElement;
    const firstRow = compiled.querySelectorAll('tr')[1];
    expect(firstRow.querySelector('td').textContent).toContain('Test 1');

    // check the rows count using the class row
    const rows = compiled.querySelectorAll('.row');
    expect(rows.length).toBe(2);

});
```

## food-container.component.spec.ts

```typescript
let component: FoodContainerComponent;
let fixture: ComponentFixture<FoodContainerComponent>;
let spy: any;

beforeEach(() => {
  const mockFoodData = [
    { id: 1, name: 'Pizza', price: 10, calories: 1200 },
    { id: 2, name: 'Burger', price: 8, calories: 800 },
    { id: 3, name: 'Salad', price: 6, calories: 300 }
  ];
  spy = jasmine.createSpyObj('FoodService', ['getFood']);
  spy.getFood.and.returnValue(of(mockFoodData));

  fixture = TestBed.configureTestingModule({
    providers: [{ provide: FoodService, useValue: spy }],
    imports: [FoodContainerComponent]
  }).createComponent(FoodContainerComponent);

  component = fixture.componentInstance;
  fixture.detectChanges();
});

it('should create', () => {
  expect(component).toBeTruthy();
});

it('should select food item', () => {
  const mockFoodItem = { id: 4, name: 'Pasta', price: 12, calories: 600 };
  component.selectFood(mockFoodItem);
  expect(component.selected).toEqual(mockFoodItem);
});

it('should delete food item', () => {
  const mockFoodItem = { id: 4, name: 'Pasta', price: 12, calories: 600 };
  component.food = [mockFoodItem];
  component.deleteFood(mockFoodItem);
  expect(component.food).not.toContain(mockFoodItem);
  expect(component.selected).toBeNull();
});

it('should save food item', () => {
  const mockFoodItem = { id: 4, name: 'Pasta', price: 12, calories: 600 };
  component.foodSaved(mockFoodItem);
  expect(component.food).toContain(mockFoodItem);
  expect(component.selected).toBeNull();
});

it('should update existing food item', () => {
  const existingFoodItem = { id: 1, name: 'Pizza', price: 10, calories: 1200 };
  const updatedFoodItem = { id: 1, name: 'Pizza', price: 15, calories: 1200 };
  component.food = [existingFoodItem];
  component.foodSaved(updatedFoodItem);
  expect(component.food).toContain(updatedFoodItem);
  expect(component.food).not.toContain(existingFoodItem);
  expect(component.selected).toBeNull();
});
```