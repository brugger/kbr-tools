import { Component, OnInit} from '@angular/core';

import { KbrAuthentication} from '../../kbr/authentication';
import  { KbrNavigator} from '../../kbr/navigator';
import {UserInfo} from '../../kbr/authentication.model';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {

  constructor(private kbrAuthentication:KbrAuthentication,
              private kbrNavigator: KbrNavigator,
  ) { }

  ngOnInit() {
    this.kbrAuthentication.logout()
    this.kbrNavigator.base()
  }

}
