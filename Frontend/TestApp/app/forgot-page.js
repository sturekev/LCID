import { createViewModel } from './forgot-page-view-model';

export function onNavigatingTo(args) {
    const page = args.object
    page.bindingContext = createViewModel()
}

export function navigateToLogin(args) {
    const button = args.object
    const page = button.page
    page.frame.navigate("main-page")
}
