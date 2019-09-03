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
