/**
 * 统一 API 客户端
 *
 * - 自动注入 JWT
 * - 401 自动跳转登录
 * - 抛出 ApiError（含 status / code）便于页面区分错误类型
 * - 页面禁止直接使用 fetch/axios
 */

export class ApiError extends Error {
  status: number
  code: number
  constructor(message: string, status: number, code: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

// nullish coalescing: empty string → relative path (Docker/nginx proxy mode)
// set value → direct backend URL (local development)
const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function getToken(): string | null {
  try {
    const stored = localStorage.getItem('auth')
    if (stored) {
      const { token } = JSON.parse(stored)
      return token || null
    }
  } catch {
    // ignore
  }
  return null
}

async function request<T = unknown>(
  method: string,
  path: string,
  body?: unknown,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }

  const token = getToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  if (res.status === 401) {
    localStorage.removeItem('auth')
    localStorage.removeItem('user')
    if (window.location.pathname !== '/login') {
      window.location.href = '/login'
    }
    throw new ApiError('Unauthorized', 401, 401)
  }

  if (!res.ok) {
    let detail = `HTTP ${res.status}`
    let code = res.status
    try {
      const err = await res.json()
      detail = err.detail || err.message || detail
      code = err.code || code
    } catch {
      // use defaults
    }
    throw new ApiError(detail, res.status, code)
  }

  return res.json()
}

export const api = {
  get<T = unknown>(path: string): Promise<T> {
    return request<T>('GET', path)
  },
  post<T = unknown>(path: string, body?: unknown): Promise<T> {
    return request<T>('POST', path, body)
  },
  delete<T = unknown>(path: string): Promise<T> {
    return request<T>('DELETE', path)
  },
}
