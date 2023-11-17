import { Observable, Fetch } from '@nativescript/core'
import { debug, openUrl } from '@nativescript/core/utils'

export function createViewModel() {
    const viewModel = new Observable()
    
  
    viewModel.forgotPassword = () => {
  
      const helpDesk = "https://www.luther.edu/offices/its/help-desk"
      openUrl(helpDesk)

    }

    return viewModel
  }
