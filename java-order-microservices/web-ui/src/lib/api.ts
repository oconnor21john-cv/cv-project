export type TokenResponse = { accessToken: string; tokenType: string }

export type OrderItem = {
  sku: string
  quantity: number
  unitPrice: number
}

export type OrderResponse = {
  id: string
  status: string
  totalAmount: number
  createdBy: string
  createdAt: string
  items: OrderItem[]
}

export type JwtPayload = {
  sub: string
  roles: string[]
  iat: number
  exp: number
}

export function apiBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8081'
}

export function decodeJwt(token: string): JwtPayload | null {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) return null
    const payload = JSON.parse(atob(parts[1]))
    return payload as JwtPayload
  } catch {
    return null
  }
}

export async function postJson<T>(url: string, body: unknown, token?: string): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`${res.status} ${res.statusText}${text ? ` — ${text}` : ''}`)
  }
  return (await res.json()) as T
}

export async function getJson<T>(url: string, token?: string): Promise<T> {
  const res = await fetch(url, {
    method: 'GET',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`${res.status} ${res.statusText}${text ? ` — ${text}` : ''}`)
  }
  return (await res.json()) as T
}

export async function deleteRequest(url: string, token?: string): Promise<void> {
  const res = await fetch(url, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`${res.status} ${res.statusText}${text ? ` — ${text}` : ''}`)
  }
}

export function shortOrigin(url: string) {
  try {
    return new URL(url).host
  } catch {
    return url
  }
}
