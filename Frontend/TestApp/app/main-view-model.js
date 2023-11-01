import { Observable, Fetch } from '@nativescript/core'
import { debug } from '@nativescript/core/utils'



export function createViewModel() {
  const viewModel = new Observable()
  viewModel.set('username', "")
  viewModel.set('password', "")

  viewModel.logIn = () => {
    fetch("")
    .then((response) => response.json())
    .then((r) => {
      viewModel.set("origin", r.count)
    }).catch((err) => {
    })
    viewModel.usr =  viewModel.get('username')
    viewModel.pass = viewModel.get('password')
    viewModel.set('debug', `user: ${viewModel.usr} Password: ${viewModel.pass}`)
  }

  return viewModel
}

