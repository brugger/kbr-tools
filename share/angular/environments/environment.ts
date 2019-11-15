// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

import { setup } from  './setup'

export const environment = {
  production: false,
  api_base: `http://localhost/${setup.name}/api`,
  url_base: `http://localhost/${setup.name}-web`,
  login_url: `http://localhost/${setup.name}/api/authorize?response_type=token&client_id=abc&scope=scope_write&redirect_uri=` + encodeURIComponent(`http://localhost/${setup.name}-web/#/login`)};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
