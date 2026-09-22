import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideMockStore } from '@ngrx/store/testing';
import { NavbarComponent } from './navbar.component';
import { NavItem } from './nav-item.model';

describe('NavbarComponent', () => {
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [NavbarComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideMockStore(),
      ],
    });

    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should have four menu items by default', (done) => {
    const fixture = TestBed.createComponent(NavbarComponent);
    const comp = fixture.componentInstance;

    const navItems: NavItem[] = [
      { title: 'Home', url: '/' },
      { title: 'Food', url: '/food' },
      { title: 'Catalog', url: '/food/catalog' },
      { title: 'About', url: '/about' },
    ];

    comp.menuItems.subscribe((items) => {
      expect(items.length).toBe(4);
      done();
    });

    httpMock.expectOne('/assets/nav-items.json').flush(navItems);
  });
});
