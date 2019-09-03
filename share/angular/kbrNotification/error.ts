import {Component, Inject, OnInit} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import {FormBuilder, Validators, FormGroup} from "@angular/forms";

@Component({
  selector: 'error-dialog',
  templateUrl: './error.html',
  styleUrls: ['./error.css']
})
export class ErrorDialogComponent implements OnInit {

  form: FormGroup;
  description:string;
  data:any;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<ErrorDialogComponent>,
    @Inject(MAT_DIALOG_DATA) {data}:any ) {

      this.description = data;
      this.data = data;

      this.form = fb.group({
      //  description: [description, Validators.required],
       // category: [category, Validators.required],

       // longDescription: [longDescription,Validators.required]
    });

  }

  ngOnInit() {

  }

  save() {
    this.dialogRef.close(this.form.value);
    return true;
  }

  close() {
    this.dialogRef.close();
    return false;
  }

}
