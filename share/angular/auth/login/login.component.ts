import { Component, OnInit } from '@angular/core';
import {HTTP_INTERCEPTORS, HttpClient} from '@angular/common/http';
import {ActivatedRoute} from '@angular/router';

import {KbrAuthentication} from '../../kbr/authentication';
import {UserInfo} from '../../kbr/authentication.model';
import {KbrNavigator} from '../../kbr/navigator';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  params = {};

  constructor( private activatedRoute: ActivatedRoute,
               private http: HttpClient,
               private kbrAuthentication: KbrAuthentication,
               private kbrNavigator: KbrNavigator,
  ) { }

  ngOnInit() {
    this.login_user();
  }

  login_user(): void {
    if (this.kbrAuthentication.isLoggedIn) {
      this.kbrNavigator.base();
    }

    this.activatedRoute.fragment.subscribe((fragment: string) => {
        fragment = fragment.substr(7);
        for (var keyVal of fragment.split("&")) {
          var split = keyVal.split("=");
          if (split.length == 2) {
            this.params[split[0]] = split[1];
          }
        }
        if (fragment.includes("token")) {
          let access_token = this.params['token'];
          //console.log('Access_token: ' + access_token);

          this.kbrAuthentication.loginUser(access_token);
          this.kbrNavigator.base();
        } else {
          console.error("token not found");
        }
      });
    }
}

