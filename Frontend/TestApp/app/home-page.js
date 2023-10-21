import { createViewModel } from './main-view-model';

export function onNavigatingTo(args) {
  const page = args.object
  page.bindingContext = createViewModel()
}

export function navigateToMain(args){
  const button = args.object
  const page = button.page
  page.frame.navigate('main-page')
}

export function onLogout(args) {
  const button = args.object
  const page = button.page
  page.frame.navigate('main-page')
}