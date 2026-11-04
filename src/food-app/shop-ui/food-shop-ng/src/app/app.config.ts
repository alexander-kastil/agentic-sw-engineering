import { ApplicationConfig, ErrorHandler, LOCALE_ID, inject, provideAppInitializer } from '@angular/core';
import { provideRouter, withEnabledBlockingInitialNavigation } from '@angular/router';
import { provideHttpClient, withInterceptors, withXhr } from '@angular/common/http';
import { provideZoneChangeDetection } from '@angular/core';
import { importProvidersFrom } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { EntityDataModule } from '@ngrx/data';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { MatSidenavModule } from '@angular/material/sidenav';
import { apimInterceptor } from './apim.interceptor';
import { ErrHandlerService } from './shared/err-handler/err-handler.service';
import { reducers, metaReducers } from './state/state';
import { MsalAuthUtilModule } from './auth/msal-auth-util.module';
import { environment } from '../environments/environment';
import { routes } from './app.routes';
import { ThemeService } from './shared/theme/theme.service';
import { cartFeature } from './food/state/cart/cart.state';
import { cartEffects } from './food/state/cart/cart.effects';

export const appConfig: ApplicationConfig = {
    providers: [
        provideZoneChangeDetection({ eventCoalescing: true }),
        provideAppInitializer(() => {
            inject(ThemeService);
        }),
        provideRouter(routes, withEnabledBlockingInitialNavigation()),
        provideHttpClient(withXhr(), withInterceptors([apimInterceptor])),
        { provide: LOCALE_ID, useValue: 'de' },
        { provide: ErrorHandler, useClass: ErrHandlerService },
        importProvidersFrom(
            BrowserAnimationsModule,
            FormsModule,
            ReactiveFormsModule,
            StoreModule.forRoot(reducers, {
                metaReducers,
                runtimeChecks: {
                    strictStateImmutability: true,
                    strictActionImmutability: true,
                },
            }),
            StoreModule.forFeature(cartFeature),
            EffectsModule.forRoot([cartEffects]),
            EntityDataModule.forRoot({}),
            !environment.production ? StoreDevtoolsModule.instrument({ connectInZone: true }) : [],
            MsalAuthUtilModule,
            MatSidenavModule
        )
    ]
};
