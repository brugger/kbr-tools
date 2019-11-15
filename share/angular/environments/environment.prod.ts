
const project:string = "CHANGE-ME";
const domain:string = "bruggercorp.com";

import { setup } from  './setup'


export const environment = {
  production: true,
  api_base: `https://${project}./api`,
  url_base: `https://${setup.domain}`,
  login_url: `https://${setup.domain}/api/authorize?response_type=token&client_id=abc&scope=scope_write&redirect_uri=` + encodeURIComponent(`https://${setup.domain}/#/login`)


};
