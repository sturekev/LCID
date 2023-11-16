import { createViewModel } from './home-view-model';

export function onNavigatingTo(args) {
  const page = args.object
  page.bindingContext = createViewModel()
}

export function onLogout(args) {
  const button = args.object
  const page = button.page
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
