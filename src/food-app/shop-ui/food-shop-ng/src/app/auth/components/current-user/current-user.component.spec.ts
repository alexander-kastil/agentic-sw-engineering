import { ComponentFixture, TestBed } from '@angular/core/testing';

import { of } from 'rxjs';
import { CurrentUserComponent } from './current-user.component';
import { MsalAuthFacade } from '../../state/auth.facade';

describe('CurrentUserComponent', () => {
  let component: CurrentUserComponent;
  let fixture: ComponentFixture<CurrentUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
    imports: [CurrentUserComponent],
    providers: [{ provide: MsalAuthFacade, useValue: { getUser: () => of(null) } }],
})
    .compileComponents();

    fixture = TestBed.createComponent(CurrentUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
