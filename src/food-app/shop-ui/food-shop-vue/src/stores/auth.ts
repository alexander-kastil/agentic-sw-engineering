import { defineStore } from 'pinia'
import { computed, shallowRef } from 'vue'
import { PublicClientApplication, type AccountInfo } from '@azure/msal-browser'
import { config } from '@/config'

export const useAuthStore = defineStore('auth', () => {
  const authEnabled = config.authEnabled
  const account = shallowRef<AccountInfo | null>(null)
  let msal: PublicClientApplication | null = null

  const isAuthenticated = computed(() => !authEnabled || account.value !== null)
  const user = computed(() => account.value?.username ?? '')

  async function initialize() {
    if (!authEnabled) return
    msal = new PublicClientApplication({
      auth: {
        clientId: config.auth.clientId,
        authority: config.auth.authority,
        redirectUri: config.auth.redirectUri,
      },
      cache: { cacheLocation: 'localStorage' },
    })
    await msal.initialize()
    const result = await msal.handleRedirectPromise()
    const active = result?.account ?? msal.getAllAccounts()[0] ?? null
    msal.setActiveAccount(active)
    account.value = active
  }

  async function login() {
    await msal?.loginRedirect({ scopes: config.auth.loginScopes })
  }

  async function logout() {
    await msal?.logoutRedirect()
    account.value = null
  }

  async function acquireToken(url: string) {
    if (!msal || !account.value) return null
    const resource = config.auth.protectedResources.find(([prefix]) => url.startsWith(prefix))
    if (!resource) return null
    const result = await msal.acquireTokenSilent({ scopes: resource[1], account: account.value })
    return result.accessToken
  }

  return { authEnabled, account, isAuthenticated, user, initialize, login, logout, acquireToken }
})
