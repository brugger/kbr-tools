import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';

@Component({
  selector: 'app-single-input',
  templateUrl: './single-input.component.html',
  styleUrls: ['./single-input.component.css']
})
export class SingleInputComponent implements OnInit {

  public title:string="Enter input";
  public placeholder:string = "Input";
  public input:string = '';

  constructor( private dialogRef: MatDialogRef<SingleInputComponent>,
               @Inject(MAT_DIALOG_DATA) private data:{} ) {

    if (data['title']) {
      this.title = data['title'];
    }
    if (data['placeholder']) {
      this.placeholder = data['placeholder'];
    }

  }


  ngOnInit() {
  }

  save(): void {
    console.log( 'saving filter', this.input)
    this.dialogRef.close( this.input );
  }

  close() {
    this.dialogRef.close( );
  }

}
