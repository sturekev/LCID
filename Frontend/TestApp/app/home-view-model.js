import { Observable, Fetch } from '@nativescript/core'
import { debug } from '@nativescript/core/utils'

export function createViewModel() {
    const viewModel = new Observable()
    
  
    viewModel.logOut = () => {
      const button = args.object;
      const page = button.page;
      page.frame.navigate('main-page')
    }
  
    return viewModel
  }