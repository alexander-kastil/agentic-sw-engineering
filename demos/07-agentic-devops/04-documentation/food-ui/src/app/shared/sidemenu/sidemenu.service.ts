import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { MatDrawerMode } from '@angular/material/sidenav';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SideMenuService {
  http = inject(HttpClient);
  breakpointObserver = inject(BreakpointObserver);
  visible = signal(true);
  position = signal<MatDrawerMode>('side');

  constructor() {
    this.watchScreen.subscribe();
  }

  getSideNavVisible() {
    return computed(() => this.visible());
  }

  getSideNavPosition() {
    return computed(() => this.position());
  }

  watchScreen = this.breakpointObserver
    .observe([Breakpoints.XSmall, Breakpoints.Small])
    .pipe(
      tap((matchesBreakpoint) => {
        console.log(matchesBreakpoint);
        this.visible.set(matchesBreakpoint.matches ? false : true);
        this.position.set(matchesBreakpoint.matches ? 'over' : 'side');
      })
    );

  setSideNavEnabled(val: boolean) {
    this.visible.set(val);
  }

  adjustSidenavToScreen(mq: string): boolean {
    return mq == 'xs' ? false : true;
  }

  toggleMenuVisibility() {
    this.visible.update((val) => !val);
  }
}

