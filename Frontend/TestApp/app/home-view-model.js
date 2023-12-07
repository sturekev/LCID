import { Observable, Fetch } from '@nativescript/core'

export function createViewModel() {
    const viewModel = new Observable()
    viewModel.username = () => {  
    }
  
    return viewModel
  }