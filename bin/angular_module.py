#!/usr/bin/env python3
""" 
 creates the skeleton files for a module: CRUD + service + navigator.
 
 
 Kim Brugger (26 Aug 2019), contact: kim.brugger@uib.nok
"""

import sys
import os
import argparse
import subprocess
import pprint
pp = pprint.PrettyPrinter(indent=4)



def write_file(filename:str, content:str) -> None:
    fh = open(filename, 'w')
    fh.write( content )
    fh.close()




def mkdir( directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
        

    
def make_directories( name:str) -> None:

    mkdir("src/app/{name}s".format(name=name))
    mkdir("src/app/{name}s/{name}-view".format(name=name))
    mkdir("src/app/{name}s/{name}-list".format(name=name))
    mkdir("src/app/{name}s/{name}-edit".format(name=name))


def make_model( name:str) -> None:
    content = """export class {Name} {{
  id: number;
  name: string;
}}""".format(Name=name.capitalize())
    print( 'model...')
    write_file("src/app/{name}s/{name}.model.ts".format(name=name), content)

    
def make_navigator( name:str ):

    content = """import {{ Injectable }} from '@angular/core';
import {{Router}} from '@angular/router';

@Injectable({{
  providedIn: 'root'
}})
export class {Name}Navigator {{

  constructor( private router:Router, ) {{ }};

  listUrl(): string {{
    return '/{name}';
  }}

  listView(): boolean {{
    this.router.navigateByUrl(this.listUrl());
    return true;
  }}

  detailedUrl(id:number): string {{
    return '/{name}/'+id;
  }}

  detailedView(id:number): boolean {{
    this.router.navigateByUrl( this.detailedUrl(id) );
    return true;
  }}

  createUrl(): string {{
    return '/{name}/add';
  }}

  createView(): boolean {{
    this.router.navigateByUrl(this.createUrl());
    return true;
  }}


  editUrl(id:number): string {{
    return `/{name}/${{id}}/edit`;
  }}

  editView(id:number): boolean {{
    this.router.navigateByUrl(this.editUrl(id));
    return true;
  }}


}}
""".format( Name=name.capitalize(), name=name)

    print( 'navigator...')
    write_file("src/app/{name}s/{name}-navigator.ts".format(name=name), content)



def make_service( name:str) -> None:
    content = """import {{ Injectable }} from '@angular/core';
import {{ HttpClient}} from '@angular/common/http';
import {{ Observable }} from 'rxjs';

import {{{Name}}} from './{name}.model';


@Injectable({{providedIn: 'root'}})

export class {Name}Service {{

  constructor( private http: HttpClient, ) {{}};

  private {name}Url = 'api/{name}';

  get{Name}s(): Observable<{Name}[]> {{
    return this.http.get<{Name}[]>(`${{this.{name}Url}}`);
  }};

  get{Name}({name}_id:number): Observable<{Name}> {{
    return this.http.get<{Name}>(`${{this.{name}Url}}/${{{name}_id}}`);
   }};

  delete{Name}({name}_id:number): Observable<any> {{
    return this.http.delete(`${{this.{name}Url}}/${{{name}_id}}`);
  }};

  add{Name}({name}:{Name}): Observable<{Name}> {{
    return this.http.post<{Name}>(`${{this.{name}Url}}`, {name});
  }}

  update{Name}({name}:{Name}): Observable<{Name}> {{
    return this.http.patch<{Name}>(`${{this.{name}Url}}/${{{name}.id}}`, {name});
  }}

}}
""".format( Name=name.capitalize(), name=name)
    print( 'service...')
    write_file("src/app/{name}s/{name}.service.ts".format(name=name), content)

def launch_cmd(cmd: str, cwd: str = "") -> None:
    effective_command = cmd
    p = subprocess.Popen(effective_command, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE,
                         bufsize=1) if cwd == '' else subprocess.Popen(effective_command, stdout=subprocess.PIPE,
                                                                       shell=True, stderr=subprocess.PIPE, bufsize=1,
                                                                       cwd=cwd)
    stdout, stderr = p.communicate()
    p_status = p.wait()
    return (p_status, stdout, stderr)


    
def make_list(name:str) -> None:

    print( 'list component...')

    launch_cmd("ng g c {name}s/{name}-list".format(name=name))
    content = """import {{ Component, OnInit }} from '@angular/core';

import {{{Name}}} from '../{name}.model';
import {{ {Name}Service}} from '../{name}.service';
import {{{Name}Navigator}} from '../{name}-navigator';

@Component({{
  selector: 'app-{name}-list',
  templateUrl: './{name}-list.component.html',
  styleUrls: ['./{name}-list.component.css']
}})
export class {Name}ListComponent implements OnInit {{

  {name}s: {Name}[];

  constructor( private {name}Service: {Name}Service,
               public {name}Navigator: {Name}Navigator,
  ) {{ }}

  ngOnInit() {{
    this.get{Name}s();
  }}
  get{Name}s(): void {{
    this.{name}Service.get{Name}s()
      .subscribe({name}s => this.{name}s = {name}s);
  }}

  delete{Name}( {name}: {Name} ):void {{
    // delete at backend
    this.{name}Service.delete{Name}( {name}.id ).subscribe();
    //delete in stored array (should be reloading of page/view instead?)
    this.{name}s = this.{name}s.filter(d => d !== {name});
  }}

}}
""".format( Name=name.capitalize(), name=name)
    write_file("src/app/{name}s/{name}-list/{name}-list.component.ts".format( Name=name.capitalize(), name=name), content)


def make_view(name:str) -> None:

    print( 'view component...')

    launch_cmd("ng g c {name}s/{name}-view".format(name=name))
    content = """
import {{ Component, OnInit }} from '@angular/core';
import {{ ActivatedRoute }} from '@angular/router';

import {{ Router }} from '@angular/router';

import {{ {Name} }} from '../{name}.model';
import {{ {Name}Service}} from '../{name}.service';
import {{{Name}Navigator}} from '../{name}-navigator';

@Component({{
  selector: 'app-{name}-view',
  templateUrl: './{name}-view.component.html',
  styleUrls: ['./{name}-view.component.css']
}})
export class {Name}ViewComponent implements OnInit {{

  {name}: {Name};
  dataloaded: boolean = false;

  constructor( private {name}Service: {Name}Service,
               private route: ActivatedRoute,
               public {name}Navigator: {Name}Navigator,
  ) {{ }}

  ngOnInit() {{
    this.get{Name}();
  }}

  get{Name}(): void {{
    const id = +this.route.snapshot.paramMap.get('id');
    //console.log( id );
    this.{name}Service.get{Name}( id )
        .subscribe({name} => {{this.{name} = {name}; this.dataloaded=true;}});
  }}

}}
""".format( Name=name.capitalize(), name=name)
    write_file("src/app/{name}s/{name}-view/{name}-view.component.ts".format( Name=name.capitalize(), name=name), content)



def make_edit(name:str) -> None:

    print( 'edit component...')

    launch_cmd("ng g c {name}s/{name}-edit".format(name=name))
    content = """
import {{ Component, OnInit }} from '@angular/core';


import {{{Name}}} from '../{name}.model';
import {{ {Name}Service}} from '../{name}.service';
import {{{Name}Navigator}} from '../{name}-navigator';
import {{ActivatedRoute}} from '@angular/router';

@Component({{
  selector: 'app-{name}-edit',
  templateUrl: './{name}-edit.component.html',
  styleUrls: ['./{name}-edit.component.css']
}})
export class {Name}EditComponent implements OnInit {{

  public {name}: {Name};

  constructor( private {name}Service: {Name}Service,
               private route: ActivatedRoute,
               public {name}Navigator: {Name}Navigator,
               ) {{ }}


  ngOnInit() {{
    this.edit_or_create();
  }}

  edit_or_create(): void {{
    const {name}Id = +this.route.snapshot.paramMap.get('id');
    if ({name}Id) {{
      this.{name}Service.get{Name}({name}Id).subscribe({name} => {{
        this.{name} = {name}
      }});
    }}
  }}


  add(name: string): void {{
    name = name.trim();
    if (!name) {{ return; }}
    this.{name}Service.add{Name}({{ name }} as {Name})
      .subscribe();

    this.{name}Navigator.listView();
  }}

  update({name}: {Name}): void {{
    this.{name}Service.update{Name}({name})
      .subscribe();

    this.{name}Navigator.listView();
  }}


}}
""".format( Name=name.capitalize(), name=name)
    write_file("src/app/{name}s/{name}-edit/{name}-edit.component.ts".format( Name=name.capitalize(), name=name), content)

    
    
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='angular module creator (CRUD + Navigator + service)')
    parser.add_argument('name', metavar='name', nargs=1, help="top name of module")

    args = parser.parse_args()
    name = args.name[ 0 ].lower()
    print( "Creating skeleton files for module: {name}".format( name=name ) )
    make_directories( name )
    make_navigator( name )
    make_service( name )
    make_model( name )
    make_view(name )
    make_list(name )
    make_edit(name )
