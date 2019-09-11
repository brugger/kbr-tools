import {{Injectable}} from '@angular/core';
import {{Router}} from '@angular/router';
import {{MatDialog, MatDialogConfig, MatDialogRef}} from '@angular/material';
import {{{Name}EditComponent}} from './{name}-edit/{name}-edit.component';
import {{ConfirmationComponent}} from '../kbrNotification/confirmation/confirmation.component';

@Injectable({{
  providedIn: 'root'
}})
export class {Name}Navigator {{

  constructor( private router:Router,
               private dialog: MatDialog,
               )
  {{ }};

  listUrl(): string {{
    return '/{name}s';
  }}

  listView(): boolean {{
    this.router.navigateByUrl(this.listUrl());
    return true;
  }}

  detailedUrl(id:number): string{{
    return '/{name}s/'+id;
  }}

  detailedView(id:number): boolean{{
    this.router.navigateByUrl( this.detailedUrl(id) );
    return true;
  }}

  createUrl(): string{{
    return '/{name}s/add';
  }}

  createView(): boolean {{
    this.router.navigateByUrl(this.createUrl());
    return true;
  }}


  editUrl(id:number): string{{
    return `/{name}s/${{id}}/edit`;
  }}


  editView({name}Id:number): MatDialogRef<{Name}EditComponent> {{
    let dialogConfig = new MatDialogConfig();
    dialogConfig.data = {name}Id;
    const dialogRef = this.dialog.open({Name}EditComponent,
                                       dialogConfig);
    return dialogRef;
   }}

  deleteView( {name}: {Name} ):MatDialogRef<ConfirmationComponent> {{
    // delete at backend

    let dialogConfig = new MatDialogConfig();
    dialogConfig.data = "Delete {name} " + {name}.name;
    dialogConfig.role = 'alertdialog';

    let dialogRef = this.dialog.open(ConfirmationComponent,
                                     dialogConfig);
    return dialogRef;
  }}

}}
