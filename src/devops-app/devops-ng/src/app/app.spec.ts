import { TestBed } from '@angular/core/testing';
import { provideZonelessChangeDetection } from '@angular/core';
import { App } from './app';

describe('App Component', () => {

  it('renders heading text', async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideZonelessChangeDetection()]
    });
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();

    const h1: HTMLHeadingElement | null = fixture.nativeElement.querySelector('h1');
    expect(h1).toBeTruthy();
    expect(h1!.textContent).toBe('Angular Food Shop');
  });

  it('renders image with correct src', async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideZonelessChangeDetection()]
    });
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();

    const img: HTMLImageElement | null = fixture.nativeElement.querySelector('img');
    expect(img).toBeTruthy();
    // In jsdom, getAttribute('src') reflects the literal template value
    expect(img!.getAttribute('src')).toBe('food.png');
  });

  it('increments count on button click', async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideZonelessChangeDetection()]
    });
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();

    const button: HTMLButtonElement | null = fixture.nativeElement.querySelector('button');
    const p: HTMLParagraphElement | null = fixture.nativeElement.querySelector('p');

    expect(button).toBeTruthy();
    expect(p).toBeTruthy();
    expect(p!.textContent).toContain('Button clicked 0 times');

    // Simulate user click
    button!.click();
    // For zoneless: Use await fixture.whenStable() instead of fixture.detectChanges()
    await fixture.whenStable();

    expect(p!.textContent).toContain('Button clicked 1 times');
  });
});
