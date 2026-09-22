import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MsalBroadcastService } from '@azure/msal-angular';
import { provideMockStore } from '@ngrx/store/testing';

import { CurrentUserComponent } from './current-user.component';
import { MsalAuthFacade } from '../../state/auth.facade';
import { MsalBroadcastServiceMock } from '../../mocks/MsalBroadcastService.mock';
import { authFeatureKey, MsalAuthState } from '../../state/auth.reducer';

describe('CurrentUserComponent', () => {
  let component: CurrentUserComponent;
  let fixture: ComponentFixture<CurrentUserComponent>;

  beforeEach(async () => {
    const initialAuthState: MsalAuthState = {
      authResponse: null,
      authEnabled: false,
    };

    await TestBed.configureTestingModule({
      imports: [CurrentUserComponent],
      providers: [
        MsalAuthFacade,
        provideMockStore({
          initialState: { [authFeatureKey]: initialAuthState },
        }),
        { provide: MsalBroadcastService, useClass: MsalBroadcastServiceMock },
      ],
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
