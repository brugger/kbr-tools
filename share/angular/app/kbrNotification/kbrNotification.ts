import {Component, Injectable} from '@angular/core';
import { MatDialog, MatDialogConfig } from "@angular/material/dialog";
import {MatSnackBar} from '@angular/material';


@Injectable({providedIn: 'root'})

export class KbrNotification {

  constructor( private dialog: MatDialog,
               private matSnackBar : MatSnackBar,
  ) {};

/*
  showDialog(diaglogType: any, data: any ){
    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;

    dialogConfig.data = {
      'description':'d', 'longDescription':'ld', 'category':'C'
    };
    dialogConfig.data = data;
    const dialogRef = this.dialog.open(diaglogType,
      dialogConfig);

  }

  errorAcknowledge(message:string): void {
//    this.showDialog( ErrorAcknowledgeDialogComponent, {'msg': 'This is an error ...'});
  }

  Acknowledgement(message:string): void {
//    let res = this.showDialog( ErrorAcknowledgeDialogComponent, {'msg': 'This is an error ...'});
    //return res;
  }


 */

  notification(message:string): void {
    if (message == undefined || message == '') { return }

    let snackBarRef = this.matSnackBar.open(message, '', {duration: 3000, panelClass:['snackbar-green']});
    //this.showDialog( ErrorDialogComponent, {'msg': 'This is an error ...'});
  }

  actionConfirm(message:string): void {
    if (message == undefined ||message == '') { return }
    let snackBarRef = this.matSnackBar.open(message, 'Ok', {duration: 300000, panelClass:['snackbar-green']});
    if (!snackBarRef.onAction().subscribe(() => {
      console.log('The snack-bar action was triggered!');
    })) {
      console.log('snackbar dismissed...' )

    }

  }

  error(message:string): void {
    if (message == undefined ||message == '') { return }
    let snackBarRef = this.matSnackBar.open(message, '', {duration: 3000, panelClass:['snackbar-red']});
    //this.showDialog( ErrorDialogComponent, {'msg': 'This is an error ...'});
  }

  errorAck(message:string): void {
    if (message == undefined ||message == '') { return }
    let snackBarRef = this.matSnackBar.open(message, 'Ok', {duration: -1, panelClass:['snackbar-red']});
    //this.showDialog( ErrorDialogComponent, {'msg': 'This is an error ...'});
  }

}


