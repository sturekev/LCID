import { Observable, Fetch } from '@nativescript/core'
import { debug } from '@nativescript/core/utils'



export function createViewModel() {
  const viewModel = new Observable()
  viewModel.set('username', "")
  viewModel.set('password', "")

  viewModel.logIn = () => {
    // fetch("")
    // .then((response) => response.json())
    // .then((r) => {
    //   viewModel.set("origin", r.count)
    // }).catch((err) => {
    // })
    viewModel.usr =  viewModel.get('username')
    viewModel.pass = viewModel.get('password')
    fetch("https://httpbin.org/post", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        username: viewModel.get('username'),
        password: viewModel.get('password')
    })
}).then((r) => r.json())
    .then((response) => {
        const result = response.json
        viewModel.set('origin', result.username)
    }).catch((e) => {
    })
    
    viewModel.set('debug', `user: ${viewModel.usr} Password: ${viewModel.pass}`)

    
    
  }

  return viewModel
}

