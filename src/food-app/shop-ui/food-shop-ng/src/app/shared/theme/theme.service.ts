import { DOCUMENT } from '@angular/common';
import { Injectable, inject, signal } from '@angular/core';

export type Theme = 'light' | 'dark';

const STORAGE_KEY = 'food-shop-theme';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private document = inject(DOCUMENT);
  private state = signal<Theme>(this.initialTheme());

  readonly theme = this.state.asReadonly();

  constructor() {
    this.apply(this.state());
  }

  toggle() {
    const next: Theme = this.state() === 'dark' ? 'light' : 'dark';
    this.state.set(next);
    localStorage.setItem(STORAGE_KEY, next);
    this.apply(next);
  }

  private initialTheme(): Theme {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }
    return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  private apply(theme: Theme) {
    this.document.documentElement.setAttribute('data-theme', theme);
  }
}
