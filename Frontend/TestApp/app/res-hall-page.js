import { createViewModel } from './main-view-model';
import {ImageSource, Image, Http } from '@nativescript/core';
import { getString, setString, remove } from '@nativescript/core/application-settings';
import { QrGenerator } from 'nativescript-qr-generator';
var getRequests = require("./apiUrls")

export function onNavigatingTo(args) {
  const page = args.object
  page.bindingContext = createViewModel()
}

export function onLogout(args) {
    const button = args.object
    const page = button.page
    remove('access_token')
    remove('hall_token')
    page.frame.navigate('main-page')
  }
 
  export function onDiningService(args) {
    const button = args.object
    const page = button.page
    page.frame.navigate('dining-service-page')
  }
  
  export function onLibraryCheckout(args) {
    const button = args.object
    const page = button.page
    page.frame.navigate('library-checkout-page')
  }


export function letMeIn(args) {
  Http.request({
    url: getRequests.apiHallAccess,
    method: 'GET',
    headers: { 'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + getString('access_token')},
  }).then(response => {
    var result = response.content.toJSON();
    var res = result.message
    if(res != null){ 
      console.log('test')
      setString('hall_token', res)
      const button = args.object
      const page = button.page
      const image = page.getViewById("qr-code")
      var token = getString('hall_token')
      console.log(token)
      const result = new QrGenerator().generate(token, {
        logo: {
            path: "../App_Resources/Android/src/main/res/drawable-hdpi/qr.png",
            ratio: {
                w: 50, h: 50
            }
        }
    });
    image.imageSource = new ImageSource(result);
    }
    else{
      viewModel.set('debug', ` resToken: ${result}`);
      console.log(result)
    }
  }, error => {
      console.error(error); 
  });   
    // const button = args.object
    // const page = button.page
    // const image = page.getViewById("qr")
    // var token = getString('hall_token')
    // const result = new QrGenerator().generate(token, {
    //     logo: {
    //         path: "../App_Resources/Android/src/main/res/drawable-hdpi/qr.png",
    //         ratio: {
    //             w: 50, h: 50
    //         }
    //     }
    // });
    // image.imageSource = new ImageSource(result);
}