import {{Injectable}} from '@angular/core';
import {{Router}} from '@angular/router';

@Injectable({{
  providedIn: 'root'
}})
export class {Name}Navigator {{

  constructor( private router:Router,
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

  editView(id:number): boolean {{
    this.router.navigateByUrl(this.editUrl(id));
    return true;
  }}

}}
