import {Injectable} from '@angular/core';
import {UserInfo} from './authentication.model';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';

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
    let url = `${environment.api_base}/me`;

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

  canCreate(endpoint:string) :boolean {
    console.log('Can user create:', endpoint)
//    console.log( 'userInfo', this.userInfo )
    if ( this.userInfo && this.userInfo.acls ) {
      if (this.userInfo.acls[endpoint]) {
        return this.userInfo.acls[endpoint]['can_create'];
      }
    }
    return false
  }


  canRead(endpoint:string) :boolean {
    console.log('Can user view:', endpoint)
//    console.log( 'userInfo', this.userInfo )
    if ( this.userInfo && this.userInfo.acls ) {
        if (this.userInfo.acls[endpoint]) {
          return this.userInfo.acls[endpoint]['can_read'];
        }
    }
    return false
  }

  canUpdate(endpoint:string) :boolean {
    console.log('Can user update:', endpoint)
 //   console.log( 'userInfo', this.userInfo )
    if ( this.userInfo && this.userInfo.acls ) {
      if (this.userInfo.acls[endpoint]) {
        return this.userInfo.acls[endpoint]['can_update'];
      }
    }
    return false
  }

  canDelete(endpoint:string) :boolean {
    console.log('Can user delete:', endpoint)
 //   console.log( 'userInfo', this.userInfo )
    if ( this.userInfo && this.userInfo.acls ) {
      if (this.userInfo.acls[endpoint]) {
        return this.userInfo.acls[endpoint]['can_delete'];
      }
    }
    return false
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

