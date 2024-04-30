import { Observable } from '@nativescript/core'
import {Http } from '@nativescript/core';
import { getString } from '@nativescript/core/application-settings'
var getRequests = require("./apiUrls")

export function createViewModel() {
    const viewModel = new Observable()
    viewModel.username = () => {  
    }
    viewModel.set('name', 'Name: John Doe')
    viewModel.set('sid', 'Student ID: 00123456')
    viewModel.set('dorm', 'Residence: Campus House')
    viewModel.set('swipes', 'Meal Swipes: 19')
    viewModel.set('dinedlrs', 'Dining Dollars: 350')
    Http.request({
      url: getRequests.apiDashboardInfo,
      method: 'GET',
      headers: { 'Content-Type' : 'application/json', 'Authorization' : 'Bearer ' + getString('access_token')},
    }).then(response => {
      var result = response.content.toJSON();
      if(result != null){ 
        viewModel.set('name', `Name: ${result.full_name}`)
        viewModel.set('sid', `Student ID: ${result.student_id}`)
        viewModel.set('dorm', `Residence: ${result.residence}`)
        viewModel.set('swipes', `Meal Swipes: ${result.swipes}`)
        viewModel.set('dinedlrs', `Dining Dollars: ${result.dining_dolars}`)
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