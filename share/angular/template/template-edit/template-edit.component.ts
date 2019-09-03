import {{ Component, Inject, OnInit }} from '@angular/core';
import {{ {Name} }} from '../{name}.model';
import {{{Name}Service}} from '../{name}.service';
import {{ActivatedRoute}} from '@angular/router';
import {{MAT_DIALOG_DATA, MatDialogRef}} from '@angular/material';

@Component({{
  selector: 'app-{name}-edit',
  templateUrl: './{name}-edit.component.html',
  styleUrls: ['./{name}-edit.component.css']
}})
export class {Name}EditComponent implements OnInit {{

  public {name}: {Name};
  private {name}_edit: boolean = false;

  constructor( private {name}Service: {Name}Service,
               private route: ActivatedRoute,
               private dialogRef: MatDialogRef<{Name}EditComponent>,
               @Inject(MAT_DIALOG_DATA) private {name}Id:number ) {{
    if ({name}Id) {{
      this.{name}Service.get{Name}({name}Id).subscribe({name} => {{
        this.{name} = {name};
        this.{name}_edit = true;
      }});
    }}

  }}

  ngOnInit() {{

  }}

  add(name: string): void {{
    name = name.trim();
    if (!name) {{ return; }}
    this.{name}Service.add{Name}({{ name }} as {Name})
      .subscribe();
    this.dialogRef.close( '{Name} added');
  }}

  update({name}: {Name}): void {{
    this.{name}Service.update{Name}({name})
      .subscribe();
    this.dialogRef.close( '{Name} updated');

  }}

  close() {{
    this.dialogRef.close( 'No {name} changes done');
  }}

}}
