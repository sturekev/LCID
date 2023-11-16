import { createViewModel } from './main-view-model';
import { getString, setString, remove } from '@nativescript/core/application-settings';

export function navigateToHome(args) {
  const button = args.object
  const page = button.page
  page.frame.navigate("home-page")
}

export function onLogout(args) {
    const button = args.object
    const page = button.page
    remove('access_token')
    remove('hall_token')
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
