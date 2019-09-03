import {Injectable} from '@angular/core';
import {UserInfo} from './authentication.model';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class KbrAuthentication {

  constructor( private http: HttpClient ) { };

  public isLoggedIn: boolean = false;
  public userInfo: UserInfo;


  storeToken(access_token:string):void{
    localStorage.setItem('access_token', access_token);
  }

  getToken():string{
    let token = localStorage.getItem('access_token');
    return token;
  }

  deleteToken():void {
    localStorage.removeItem('access_token')
  }

  prelogin():void {
    if (this.isLoggedIn){
      return;
    }

    let token = this.getToken();
    if (token) {
      this.loginUser( token );
    }
  }

  getUserInfo(token:string) : void {
    let url = "/api/user-info/";
    this.http.get<UserInfo>(url, {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    }).subscribe(userInfo => {
      this.userInfo = userInfo;

    }, error => {
      console.log(error.message);
    });
    return null;
  }


  loginUser(token:string):void {
    this.logout();
    this.getUserInfo(token);
    this.storeToken( token );
    this.isLoggedIn = true;
    console.log( 'userInfo: ' +this.userInfo );


  }

  logout():void{
    this.isLoggedIn = false;
    this.userInfo = new UserInfo();
    this.deleteToken()
  }

}

