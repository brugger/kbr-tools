import { NgModule } from '@angular/core';

import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from './auth/login/login.component';
import {LogoutComponent} from './auth/logout/logout.component';
import {WelcomeComponent} from './welcome/welcome.component';
import {AboutComponent} from './about/about.component';

const routes: Routes = [
  { path: '',                component: WelcomeComponent},
  { path: 'about',           component: AboutComponent},
  { path: 'login',           component: LoginComponent},
  { path: 'logout',          component: LogoutComponent},
];

@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(routes, {useHash: true})],
  exports: [RouterModule]
})
export class RoutingModule { }
