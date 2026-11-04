import { Component, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { filter, map, startWith, tap } from 'rxjs/operators';
import { environment } from '../environments/environment';
import { MsalAuthFacade } from './auth/state/auth.facade';
import { SidenavFacade } from './state/sidenav/sidenav.facade';

import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './menus/navbar/navbar.component';
import { SidebarComponent } from './menus/sidebar/sidebar.component';
import { LoginComponent } from './auth/components/login/login.component';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  changeDetection: ChangeDetectionStrategy.Eager,
  imports: [
    CommonModule,
    RouterOutlet,
    NavbarComponent,
    SidebarComponent,
    LoginComponent
  ]
})
export class AppComponent implements OnDestroy {
  title = environment.title;
  sidenavVisible = this.mf.getSideNavVisible();
  isIframe = window !== window.parent && !window.opener;

  authEnabled = environment.authEnabled;
  authenticated = this.af.isAuthenticated();
  isHome = this.router.events.pipe(
    startWith(null),
    filter((e) => e === null || e instanceof NavigationEnd),
    map(() => this.router.url.split(/[?#]/)[0] === '/')
  );
  publicRoute = this.router.events.pipe(
    startWith(false),
    filter((e) => e instanceof NavigationEnd),
    map((event) => {
      return event instanceof NavigationEnd && event.url.includes('about');
    }),
    tap((result) => {
      console.log('publicRoute', result);
    })
  );

  private destroy$ = new Subject();

  constructor(
    private af: MsalAuthFacade,
    public mf: SidenavFacade,
    private router: Router
  ) {
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.complete();
  }
}
