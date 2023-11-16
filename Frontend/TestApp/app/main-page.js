import { createViewModel } from './main-view-model';

export function onNavigatingTo(args) {
  const page = args.object
  page.bindingContext = createViewModel()
}

export function navigateToHome(args) {
  const button = args.object
  const page = button.page
  page.frame.navigate("home-page")
}

export function onForgotPasswordTap(args) {
  const button = args.object
  const page = button.page
  page.frame.navigate("forgot-page")
}
