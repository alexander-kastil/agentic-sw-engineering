import { Routes } from '@angular/router';
import { environment } from '../environments/environment';
import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';

// Guards placeholder: enable MSAL guard only when auth is enabled (legacy kept minimal)
// If guards are needed, they can be added directly to route definitions.

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'about', component: AboutComponent },
    {
        path: 'food',
        loadChildren: () => import('./food/food.module').then(m => m.FoodModule)
    }
];
