import {HTTP_INTERCEPTORS, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {finalize, tap} from 'rxjs/operators';

import {KbrAuthentication} from './authentication';
import {KbrNavigator} from './navigator';
import {KbrNotification} from '../kbrNotification/kbrNotification';

@Injectable({
  providedIn: 'root',
})

export class KbrHttpInterceptor implements HttpInterceptor {
  constructor( private kbrAuthentication: KbrAuthentication,
               private kbrNavigator: KbrNavigator,
               private kbrNotification: KbrNotification,) {

  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let status: number;
    let description: string;
    let msgs: string[];

    //insert authorization token if user is already logged in
    //console.log( 'injecting the token' + this.kbrAuthentication.token);

    const authReq = this.kbrAuthentication.isLoggedIn ? req.clone({
          headers: req.headers.set('Authorization', 'Bearer ' + this.kbrAuthentication.getToken())
        }) : req;

    return next.handle(authReq)
      .pipe(
        tap(
          event => {
            console.log( event );
          },
          // Operation failed; error is an HttpErrorResponse
          error => {
            //console.log( error );
                        status = error.status;

                        if (status == 400) {
                          msgs = [error.error.msg];
                          console.log( msgs )
                        } else {
                          description = error.description;
                        }
          }
        ),

        // Log when response observable either completes or errors
        finalize(() => {
          //console.log( 'status ' + status);
          //console.log( 'description ' + description);
          //console.log( 'msgs ' + msgs);
          switch (status) {
            case 400:
              if (!msgs || msgs === []) {
                msgs = ['Bad request'];
              }
              this.kbrNotification.error(msgs.join("\n"));
              break;
            case 401:
              if (!msgs || msgs === []) {
                msgs = ['User not authorized'];
              }
               this.kbrNavigator.logout();
              break;
            case 403:
              if (!msgs || msgs === []) {
                msgs = ['Forbidden'];
              }
              this.kbrNotification.error(msgs.join("\n"));
              //              this.kbrNavigator.accessDenied();
              break;
            case 404:
              if (!msgs || msgs === []) {
                msgs = ['Resource(s) not found'];
              }
              this.kbrNotification.error(msgs.join("\n"));
//              this.kbrNavigator.notFound();
              break;
            case 503:
              this.kbrNotification.errorAck("Unable to contact remote server. Make sure your connection is working and try again");
              break;
            default:
              //handle remaining 4xx or 5xx responses
             if (status / 100 > 3) {
                this.kbrNotification.errorAck(description);
              }
              break;
          }
        })
      );
  }
}

/** Http interceptor providers in outside-in order */
export const httpInterceptorProviders = [
  {provide: HTTP_INTERCEPTORS, useClass: KbrHttpInterceptor, multi: true},
];
