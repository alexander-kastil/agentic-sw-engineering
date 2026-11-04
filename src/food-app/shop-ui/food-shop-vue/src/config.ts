const runtime = import.meta.env.PROD ? (window.env ?? {}) : {}
const env = import.meta.env

const withoutTrailingSlash = (url: string) => url.replace(/\/+$/, '')

const catalogApi = withoutTrailingSlash(runtime.CATALOG_API_URL || env.VITE_CATALOG_API_URL)

export const config = {
  title: 'Food Shop',
  catalogApi,
  ordersApi: withoutTrailingSlash(runtime.ORDERS_API_URL || env.VITE_ORDERS_API_URL),
  authEnabled: String(runtime.AUTH_ENABLED || env.VITE_AUTH_ENABLED) === 'true',
  apimKey: runtime.APIM_KEY || env.VITE_APIM_KEY,
  applicationInsights: runtime.APPLICATION_INSIGHTS || env.VITE_APPLICATION_INSIGHTS,
  auth: {
    clientId: runtime.CLIENT_ID || env.VITE_CLIENT_ID,
    authority: runtime.AUTHORITY || env.VITE_AUTHORITY,
    redirectUri: runtime.REDIRECT_URI || env.VITE_REDIRECT_URI,
    loginScopes: ['user.read'],
    protectedResources: [
      ['https://graph.microsoft.com/v1.0/me', ['user.read']],
      [`${catalogApi}/food`, ['api://b509d389-361a-447b-afb2-97cc8131dad6/access_as_user']],
    ] as [string, string[]][],
  },
}
