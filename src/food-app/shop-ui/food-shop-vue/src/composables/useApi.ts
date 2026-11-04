import { config } from '@/config'
import { useAuthStore } from '@/stores/auth'

export function useApi() {
  const auth = useAuthStore()

  async function request<T>(method: string, url: string, body?: unknown): Promise<T> {
    const headers = new Headers({ 'Ocp-Apim-Subscription-Key': config.apimKey })
    const token = await auth.acquireToken(url)
    if (token) headers.set('Authorization', `Bearer ${token}`)
    if (body !== undefined) headers.set('Content-Type', 'application/json')

    const response = await fetch(url, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    })
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`)

    const text = await response.text()
    return (text ? JSON.parse(text) : undefined) as T
  }

  return {
    get: <T>(url: string) => request<T>('GET', url),
    post: <T>(url: string, body: unknown) => request<T>('POST', url, body),
    put: <T>(url: string, body: unknown) => request<T>('PUT', url, body),
    remove: (url: string) => request<void>('DELETE', url),
  }
}
