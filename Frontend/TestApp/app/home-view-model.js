import { Observable, Fetch } from '@nativescript/core'
import { debug } from '@nativescript/core/utils'

export function createViewModel() {
    const viewModel = new Observable()
    
  
    // viewModel.logIn = () => {
  
    //   fetch("https://httpbin.org/get")
    //   .then((response) => response.json())
    //   .then((r) => {
    //     viewModel.set("origin", r.url)
    //   }).catch((err) => {
    //   })
    //   viewModel.usr =  viewModel.get('username')
    //   viewModel.pass = viewModel.get('password')
    //   viewModel.set('debug', `user: ${viewModel.usr} Password: ${viewModel.pass}`)
    // }

    viewModel.username = () => {
      
    }
  
    return viewModel
  }