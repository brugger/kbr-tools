import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { RoutingModule } from './routing.module';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import {
  MatBadgeModule,
  MatButtonModule, MatCheckboxModule, MatChipsModule, MatDialogModule, MatExpansionModule,
  MatFormFieldModule,
  MatIconModule, MatInputModule,
  MatMenuModule, MatOptionModule, MatProgressSpinnerModule, MatRadioModule, MatRippleModule, MatSelectModule, MatSidenavModule,
  MatSnackBarModule,
  MatTableModule,
  MatToolbarModule
} from '@angular/material';
import { ConfirmationComponent } from './kbrNotification/confirmation/confirmation.component';
import { LoginComponent } from './auth/login/login.component';
import { LogoutComponent } from './auth/logout/logout.component';
import { httpInterceptorProviders} from './kbr/interceptor';
import { WelcomeComponent } from './welcome/welcome.component';
import { AboutComponent } from './about/about.component';
import { SingleInputComponent } from './kbrNotification/single-input/single-input.component';


@NgModule({
  declarations: [
    AppComponent,
    ConfirmationComponent,
    SingleInputComponent,
    LoginComponent,
    LogoutComponent,
    AboutComponent,
    WelcomeComponent,

  ],
  imports: [
    BrowserModule,
    RoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatSnackBarModule,
    MatExpansionModule,
    MatRippleModule,
    MatBadgeModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatCheckboxModule,
    MatOptionModule,
    MatSelectModule,
    MatSidenavModule,
    MatMenuModule,
    MatRadioModule,
    MatToolbarModule,
    MatIconModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    MatDialogModule,
    ReactiveFormsModule,
    FormsModule,

],
  providers: [httpInterceptorProviders],
  entryComponents: [ConfirmationComponent,
                    SingleInputComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
