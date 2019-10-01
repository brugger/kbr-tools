import { Component } from '@angular/core';

import { KbrAuthentication} from './kbr/authentication';
import {DomainNavigatorService} from './domains/domain-navigator.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'vmail-frontend';

  constructor( private kbrAuthentication: KbrAuthentication,
               // used in the html code
               public domainNavigatorService: DomainNavigatorService,
  ) { kbrAuthentication.prelogin()}
}
