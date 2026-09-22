import { Component, ChangeDetectionStrategy } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';

@Component({
    selector: 'app-sidemenu',
    imports: [MatToolbarModule, MatListModule],
    templateUrl: './sidemenu.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './sidemenu.component.scss'
})
export class SideMenuComponent {

}
