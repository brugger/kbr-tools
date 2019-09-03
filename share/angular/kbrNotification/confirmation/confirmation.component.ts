import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';

@Component({
  selector: 'app-confirmation',
  templateUrl: './confirmation.component.html',
  styleUrls: ['./confirmation.component.css']
})
export class ConfirmationComponent implements OnInit {

  constructor( private dialogRef: MatDialogRef<ConfirmationComponent>,
               @Inject(MAT_DIALOG_DATA) private message:string ) {
  }

  ngOnInit() {

  }


  accept() {
    this.dialogRef.close(true);
  }

  close() {
    this.dialogRef.close(false);
  }

}
