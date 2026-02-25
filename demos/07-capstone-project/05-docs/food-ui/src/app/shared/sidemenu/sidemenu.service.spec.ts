import { TestBed } from '@angular/core/testing';

import { SideMenuService } from './sidemenu.service';

describe('SidemenuService', () => {
  let service: SideMenuService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SideMenuService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
