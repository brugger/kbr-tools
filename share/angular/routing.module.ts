import { NgModule } from '@angular/core';

import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {LogoutComponent} from './login/logout/logout.component';

const routes: Routes = [
  { path: 'login',           component: LoginComponent},
  { path: 'logout',          component: LogoutComponent},
];

@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(routes, {useHash: true})],
  exports: [RouterModule]
})
export class RoutingModule { }
