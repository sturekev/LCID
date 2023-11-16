import { Observable, Http, ImageSource, Image } from '@nativescript/core'
import { getString, setString } from '@nativescript/core/application-settings'
import { navigateToHome } from '../app/main-page'
var getRequests = require("./apiUrls")


export function createViewModel() {
  const viewModel = new Observable()
  //viewModel.set('username', "")
  //viewModel.set('password', "")
  // viewModel.logIn = () => {
  //   var data = {
  //     "username": viewModel.get("username"),
  //     "password": viewModel.get("password")
  //    };
  //    var endocedStr = "";
  //    for (var prop in data) {
  //      if(endocedStr) {
  //        endocedStr += "&";
  //      } 
  //      endocedStr += prop + "=" + data[prop];
  //    }
  //   Http.request({
  //     url: getRequests.apilogin,
  //     method: 'POST',
  //     headers: { 'Content-Type' : 'application/x-www-form-urlencoded' },
  //     content: endocedStr,
  //   }).then(response => {
  //     var result = response.content.toJSON();
  //     if(result.detail){
  //       viewModel.set('debug', ` Response: ${result.access_token}`);
  //     }
  //     else{
  //       setString('access_token', result.access_token)
  //       console.log(getString('access_token'))
  //       viewModel.set('debug', ` Token: ${getString('access_token')}`)
  //       navigateToHome()
  //     }
  //   }, error => {
  //       console.error(error);
  //   });
  // }
  // viewModel.letMeIn = () => {
  //   Http.request({
  //     url: getRequests.apiHallAccess,
  //     method: 'GET',
  //     headers: { 'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + getString('access_token')},
  //   }).then(response => {
  //     var result = response.content.toJSON();
  //     if(result.message){ 
  //       console.log(result.message)
  //       setString('hall_token', result.message)
  //       GenQRCode(this) //needs to pass button on this page rather than undeifind 
  //     }
  //     else{
  //       viewModel.set('debug', ` resToken: ${result}`);
  //       console.log(result)
  //     }
  //   }, error => {
  //       console.error(error); 
  //   });   
  // }
  return viewModel
}

