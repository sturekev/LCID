import { Observable, Fetch, Http, ImageSource, Image } from '@nativescript/core'
import { getString, setString } from '@nativescript/core/application-settings'
import { QrGenerator } from 'nativescript-qr-generator';
import { debug } from '@nativescript/core/utils'
var getRequests = require("./apiUrls")


export function createViewModel() {
  const viewModel = new Observable()
  viewModel.set('username', "")
  viewModel.set('password', "")
  viewModel.logIn = () => {
    var data = {
      "username": viewModel.get("username"),
      "password": viewModel.get("password")
     };
     var endocedStr = "";
     for (var prop in data) {
       if(endocedStr) {
         endocedStr += "&";
       } 
       endocedStr += prop + "=" + data[prop];
     }
    Http.request({
      url: getRequests.apilogin,
      method: 'POST',
      headers: { 'Content-Type' : 'application/x-www-form-urlencoded' },
      content: endocedStr,
    }).then(response => {
      var result = response.content.toJSON();
      if(result.detail){
        viewModel.set('debug', ` Response: ${result.access_token}`);
      console.log(result)
      }
      else{
        setString('access_token', result.access_token)
        console.log(getString('access_token'))
        viewModel.set('debug', ` Token: ${getString('access_token')}`)
      }
    }, error => {
        console.error(error);
    });
  }
  viewModel.letMeIn = () => {
    var date = String(Date.now())
    Http.request({
      url: getRequests.apiHallAccess + `{"userToken": ${getString('access_token')}, "timestamp": ${date}}`,
      method: 'POST',
      headers: { 'Content-Type' : 'application/json' },
      content: JSON.stringify({
        userToken: getString('access_token'),
        timestamp: date
      }),
    }).then(response => {
      var result = response.content.toJSON();
      if(result.detail){
        viewModel.set('debug', ` Response: ${result.access_token}`);
        console.log(result)
      }
      else{
        viewModel.set('debug', ` resToken: ${result}`);
        console.log(result)
      }
    }, error => {
        console.error(error); 
    });   
  }
  viewModel.onImageLoadedBasic = (args) => {
    const image = args.object;
    const result = new QrGenerator().generate("test", {
        logo: {
            path: "../App_Resources/Android/src/main/res/drawable-hdpi/qr.png",
            ratio: {
                w: 50, h: 50
            }
        }
    });
    image.imageSource = new ImageSource(result);
  }
  return viewModel
}

