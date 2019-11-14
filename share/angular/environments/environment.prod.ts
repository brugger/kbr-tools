
const project:string = "CHANGE-ME";
const domain:string = "bruggercorp.com";


export const environment = {
  production: true,
  api_base: `https://${project}./api`,
  url_base: `https://${project}.${domain}`,
  login_url: `https://${project}.${domain}/api/authorize?response_type=token&client_id=abc&scope=scope_write&redirect_uri=' + encodeURIComponent('https://${project}.${domain}/#/login`)


};
