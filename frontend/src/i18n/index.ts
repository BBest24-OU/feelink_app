/**
 * Internationalization setup using svelte-i18n
 */
import { register, init, getLocaleFromNavigator, locale } from 'svelte-i18n';

// Register translation files
register('en', () => import('./en.json'));
register('pl', () => import('./pl.json'));

// Initialize i18n
export function initI18n() {
  init({
    fallbackLocale: 'en',
    initialLocale: getLocaleFromNavigator(),
  });
}

// Export locale store for use in components
export { locale, _ as t } from 'svelte-i18n';
