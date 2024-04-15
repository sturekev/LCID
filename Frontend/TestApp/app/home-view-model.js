import { Observable, Fetch } from '@nativescript/core'
import {Http } from '@nativescript/core';
import { getString, setString } from '@nativescript/core/application-settings'
var getRequests = require("./apiUrls")

export function createViewModel() {
    const viewModel = new Observable()
    viewModel.username = () => {  
    }
    viewModel.set('dorm', 'test')
    Http.request({
      url: getRequests.apiDashboardInfo,
      method: 'GET',
      headers: { 'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + getString('access_token')},
    }).then(response => {
      var result = response.content.toJSON();
      var res = result.message
      console.log(res)
      if(res != null){ 
        viewModel.set('name', `Name: ${res.full_name}`)
        viewModel.set('sid', `Student ID: ${res.student_id}`)
        viewModel.set('dorm', `Residence: ${res.residence}`)
        viewModel.set('swipes', `Meal Swipes: ${res.swipes}`)
        viewModel.set('dinedlrs', `Dining Dollars: ${res.dining_dolar}`)
      }
      else{
        viewModel.set('debug', ` resToken: ${result}`);
        console.log(result)
      }
    }, error => {
        console.error(error); 
    });
    return viewModel
  }