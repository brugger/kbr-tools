import {{ Component, OnInit }} from '@angular/core';

import {{{Name}}} from '../{name}.model';
import {{ {Name}Service}} from '../{name}.service';
import {{{Name}Navigator}} from '../{name}-navigator';
//import {{CourseDialogComponent}} from '../../kbrNotification/error';
import {{ MatDialog, MatDialogConfig }} from "@angular/material/dialog";
import {{KbrNotification}} from '../../kbrNotification/kbrNotification';
import {{{Name}EditComponent}} from '../{name}-edit/{name}-edit.component';
import {{ConfirmationComponent}} from '../../kbrNotification/confirmation/confirmation.component';


@Component({{
  selector: 'app-{name}-list',
  templateUrl: './{name}-list.component.html',
  styleUrls: ['./{name}-list.component.css']
}})
export class {Name}ListComponent implements OnInit {{

  {name}s: {Name}[];
  displayedColumns: string[] = ['{name}', 'action'];

  constructor( private {name}Service: {Name}Service,
               public {name}Navigator: {Name}Navigator,
               private dialog: MatDialog,
               private kbrNotification: KbrNotification,
  ) {{ }}

  ngOnInit() {{
    this.get{Name}s();
  }}

  edit{Name}({name}Id:number): void {{

    let dialogConfig = new MatDialogConfig();
    dialogConfig.data = {name}Id;
    const dialogRef = this.dialog.open({Name}EditComponent,
      dialogConfig);

    dialogRef.afterClosed().subscribe(
      message => this.kbrNotification.notification( message ),
      error => {{this.kbrNotification.error(error)}},
      () => this.get{Name}s(),
    );
  }}

  get{Name}s(): void {{
    this.{name}Service.get{Name}s()
      .subscribe({name}s => this.{name}s = {name}s);
  }}

  delete{Name}( {name}: {Name} ):void {{
    // delete at backend

     let dialogConfig = new MatDialogConfig();
     dialogConfig.data = "Delete {name} " + {name}.name;
     dialogConfig.role = 'alertdialog';

     let dialogRef = this.dialog.open(ConfirmationComponent,
        dialogConfig);

     dialogRef.afterClosed().subscribe(
        accecpted => {{
           console.log( "confirm" + accecpted );
           if (accecpted) {{
             this.{name}Service.delete{Name}({name}.id).subscribe();
             //delete in stored array (should be reloading of page/view instead?)
             this.{name}s = this.{name}s.filter(d => d !== {name});
             this.kbrNotification.notification('{Name} deleted');
          }}
        }},
     );
  }}

}}