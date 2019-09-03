import {{ Injectable }} from '@angular/core';
import {{ HttpClient}} from '@angular/common/http';
import {{ Observable }} from 'rxjs';

import {{{Name}}} from './{name}.model';


@Injectable({{providedIn: 'root'}})

export class {Name}Service {{

  constructor( private http: HttpClient, ) {{}};

  private {name}Url = 'http://localhost/api/{name}';

  get{Name}s(): Observable<{Name}[]> {{
    console.log('getting {name}s')
    return this.http.get<{Name}[]>(`${{this.{name}Url}}`);
  }};

  get{Name}({name}_id:number): Observable<{Name}> {{
    console.log('get {name}')
    return this.http.get<{Name}>(`${{this.{name}Url}}/${{{name}_id}}`);
   }};

  delete{Name}({name}_id:number): Observable<any> {{
    console.log( "deleting {name} " + {name}_id);
    return this.http.delete(`${{this.{name}Url}}/${{{name}_id}}`);
  }};

  add{Name}({name}:{Name}): Observable<{Name}> {{
    return this.http.post<{Name}>(`${{this.{name}Url}}`, {name});
  }}

  update{Name}({name}:{Name}): Observable<{Name}> {{
    console.log( "{name} update: ", {name} )
    return this.http.patch<{Name}>(`${{this.{name}Url}}/${{{name}.id}}`, {name});
  }}

}}


