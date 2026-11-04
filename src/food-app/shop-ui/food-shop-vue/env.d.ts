/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_CATALOG_API_URL: string
  readonly VITE_ORDERS_API_URL: string
  readonly VITE_AUTH_ENABLED: string
  readonly VITE_CLIENT_ID: string
  readonly VITE_AUTHORITY: string
  readonly VITE_REDIRECT_URI: string
  readonly VITE_APPLICATION_INSIGHTS: string
  readonly VITE_APIM_KEY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

interface Window {
  env?: Record<string, string | undefined>
}
