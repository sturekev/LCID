import { Http } from '@nativescript/core';
import { getString, setString, remove } from '@nativescript/core/application-settings';
var getRequests = require("./apiUrls")

export function navigateToHome(args) {
  const button = args.object
  const page = button.page
  page.frame.navigate("home-page")
}

export function onLogout(args) {
    const button = args.object
    const page = button.page
    remove('access_token')
    remove('hall_token')
    page.frame.navigate('main-page')
  }

export function onResidenceHall(args) {
  const button = args.object
  const page = button.page
  page.frame.navigate('res-hall-page')
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

export function giveMeBook(args) {
  Http.request({
    url: getRequests.apiHallAccess,
    method: 'GET',
    headers: { 'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + getString('access_token')},
  }).then(response => {
    var result = response.content.toJSON();
    var res = result.message
    if(res != null){ 
      setString('book_token', res)
      const button = args.object
      const page = button.page
      const label = page.getViewById("bc")
      var token = getString('book_token')
      //format sid stirng with '*' on either side
      label.text = "*00529194*"      
    }
    else{
      viewModel.set('debug', ` resToken: ${result}`);
      console.log(result)
    }
  }, error => {
      console.error(error); 
  }); 
}