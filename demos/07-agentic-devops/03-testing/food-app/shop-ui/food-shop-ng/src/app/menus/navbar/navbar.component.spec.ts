import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { NavbarComponent } from './navbar.component';
import { NavItem } from './nav-item.model';
import { SidenavFacade } from '../../state/sidenav/sidenav.facade';

describe('NavbarComponent', () => {
  let fixture: ComponentFixture<NavbarComponent>;
  let httpMock: HttpTestingController;
  let facade: { toggleMenuVisibility: jasmine.Spy };

  const navItems: NavItem[] = [
    { title: 'Home', url: '/' },
    { title: 'Food', url: '/food' },
    { title: 'Catalog', url: '/food/catalog' },
    { title: 'About', url: '/about' },
  ];

  beforeEach(async () => {
    facade = { toggleMenuVisibility: jasmine.createSpy('toggleMenuVisibility') };

    await TestBed.configureTestingModule({
      imports: [NavbarComponent],
      providers: [
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: SidenavFacade, useValue: facade },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(NavbarComponent);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('requests the menu items from the nav-items asset', () => {
    fixture.detectChanges();

    const req = httpMock.expectOne('/assets/nav-items.json');
    expect(req.request.method).toBe('GET');
    req.flush(navItems);
  });

  it('renders one link per menu item returned by the API', () => {
    fixture.detectChanges();
    httpMock.expectOne('/assets/nav-items.json').flush(navItems);
    fixture.detectChanges();

    const links: NodeListOf<HTMLElement> = fixture.nativeElement.querySelectorAll('.navLink');
    expect(links.length).toBe(navItems.length);
    expect(links[0].textContent).toContain('Home');
    expect(links[navItems.length - 1].textContent).toContain('About');
  });

  it('toggles the sidenav when the menu icon is clicked', () => {
    fixture.detectChanges();
    httpMock.expectOne('/assets/nav-items.json').flush(navItems);

    fixture.nativeElement.querySelector('.menu').click();

    expect(facade.toggleMenuVisibility).toHaveBeenCalled();
  });
});
