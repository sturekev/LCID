import { createViewModel } from './main-view-model';
import {Http} from '@nativescript/core'
import { getString, setString } from '@nativescript/core/application-settings'

var getRequests = require("./apiUrls")

export function onNavigatingTo(args) {
  const page = args.object
  page.bindingContext = createViewModel()
}

export function navigateToHome(args) {
  const button = args.object
  const page = button.
  page.frame.navigate("home-page")
}


export function onForgotPasswordTap(args) {
  const button = args.object
  const page = button.page
  page.frame.navigate("forgot-page")
}
export function logIn(args){
  const button = args.object
  const page = button.page
  var data = {
    "username": page.getViewById('usr').text,
    "password": page.getViewById('pass').text
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
      if(result.detail == "Incorrect username or password"){
        console.log(result)
        console.log(result.detail)
        const button = args.object
        const page = button.page
        const label = page.getViewById("errorMSG")
        label.text = result.detail
      }
      else{
        setString('access_token', result.access_token)
        console.log(getString('access_token'))
        page.frame.navigate("home-page")
      }
    }, error => {
      console.log("test2")
      console.error(error);
    });
}
