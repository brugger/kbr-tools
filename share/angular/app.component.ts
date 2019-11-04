import { Component } from '@angular/core';

import { environment } from '../environments/environment';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'APP-TITLE';

  private loginUrl    = `${environment.login_url}`;


  constructor( public kbrAuthentication: KbrAuthentication,

  ) { kbrAuthentication.prelogin()}
}
