import { createViewModel } from './main-view-model';
import { getString, setString, remove } from '@nativescript/core/application-settings';

export function onNavigatingTo(args) {
  const page = args.object
  page.bindingContext = createViewModel()
}

export function onLogout(args) {
    const button = args.object
    const page = button.page
    remove('access_token')
    remove('hall_token')
    page.frame.navigate('main-page')
  }