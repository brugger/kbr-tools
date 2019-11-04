import { Component, OnInit } from '@angular/core';
import {interval} from 'rxjs';
import {SampleNavigator} from '../samples/sample-navigator';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.css']
})
export class WelcomeComponent implements OnInit {

  public  opacity = 1.0;

  constructor( private sampleNavigator: SampleNavigator) { }

  ngOnInit() {
  }

  fade_image():void {
    const attemptsCounter = interval(10);
    let reloader = attemptsCounter.subscribe(n => {
      this.opacity -= 0.01;
      //console.log( "Opacity: ", this.opacity)
      if (this.opacity <= 0){
        reloader.unsubscribe();
        this.sampleNavigator.listView();
      }
    });
  }


}
