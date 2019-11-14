import { Injectable } from '@angular/core';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class KbrNavigator {

  constructor( private router:Router, ) { };

  goto(url:string): void{


  }


  baseUrl(): string {
    return '/';
  }

  base(): boolean {
    this.router.navigateByUrl(this.baseUrl());
    return true;
  }


  dashboardUrl(): string {
    return '/dashboard';
  }

  dashboard(): boolean {
    this.router.navigateByUrl(this.dashboardUrl());
    return true;
  }

  logoutUrl():string{
    return '/logout';
  }

  logout(): boolean {
    this.router.navigateByUrl(this.logoutUrl());
    return true;
  }

  loginUrl():string{
    return '/login';
  }

  login(): boolean {
    this.router.navigateByUrl(this.loginUrl());
    return true;
  }

  homeUrl(): string {
    return '';
  }

  homeView(): boolean {
    this.router.navigateByUrl(this.homeUrl());
    return true;
  }

  aboutUrl(): string {
    return '/about';
  }

  aboutView(): boolean {
    this.router.navigateByUrl(this.aboutUrl());
    return true;
  }



  accessDeniedUrl():string{
    return '/access-denied';
  }

  accessDenied(): boolean {
    this.router.navigateByUrl(this.accessDeniedUrl());
    return true;
  }

  notFoundUrl():string{
    return '/not-found';
  }

  notFound(): boolean {
    this.router.navigateByUrl(this.notFoundUrl());
    return true;
  }

  errorUrl():string{
    return '/not-found';
  }

  error(): boolean {
    this.router.navigateByUrl(this.errorUrl());
    return true;
  }

}
