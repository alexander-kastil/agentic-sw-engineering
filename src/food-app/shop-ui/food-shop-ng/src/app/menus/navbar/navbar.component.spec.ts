import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { NavbarComponent } from './navbar.component';
import { SidenavFacade } from '../../state/sidenav/sidenav.facade';

describe('NavbarComponent', () => {
  let comp: NavbarComponent;
  let http: HttpTestingController;
  let mf: jasmine.SpyObj<SidenavFacade>;

  beforeEach(() => {
    mf = jasmine.createSpyObj('SidenavFacade', ['toggleMenuVisibility']);
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: SidenavFacade, useValue: mf },
      ],
    });
    http = TestBed.inject(HttpTestingController);
    comp = TestBed.runInInjectionContext(() => new NavbarComponent());
  });

  it('should load three menu items by default', () => {
    let count = 0;
    comp.menuItems.subscribe((items) => (count = items.length));
    http.expectOne('/assets/nav-items.json').flush([{}, {}, {}]);
    expect(count).toBe(3);
  });

  it('should toggle the menu through the facade', () => {
    comp.toggleMenu();
    expect(mf.toggleMenuVisibility).toHaveBeenCalled();
  });
});
