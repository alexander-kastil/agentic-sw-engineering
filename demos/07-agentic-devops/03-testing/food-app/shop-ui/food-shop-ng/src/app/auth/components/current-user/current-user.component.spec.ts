import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { MsalAuthFacade } from '../../state/auth.facade';
import { CurrentUserComponent } from './current-user.component';

describe('CurrentUserComponent', () => {
  let component: CurrentUserComponent;
  let fixture: ComponentFixture<CurrentUserComponent>;

  const user = 'giro.kastil@integrations.at';

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CurrentUserComponent],
      providers: [{ provide: MsalAuthFacade, useValue: { getUser: () => of(user) } }],
    }).compileComponents();

    fixture = TestBed.createComponent(CurrentUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('renders the signed-in user', () => {
    expect(fixture.nativeElement.querySelector('h5').textContent).toContain(user);
  });
});
