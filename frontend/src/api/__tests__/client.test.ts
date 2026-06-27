import { describe, it, expect, beforeEach, vi } from 'vitest'
import { api, ApiError } from '../client'

const localStorageMock = (() => {
  let store: Record<string, string> = {}
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value },
    removeItem: (key: string) => { delete store[key] },
    clear: () => { store = {} },
  }
})()
Object.defineProperty(window, 'localStorage', { value: localStorageMock })

describe('API Client', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  it('attaches JWT Authorization header when token exists', async () => {
    localStorage.setItem('auth', JSON.stringify({ token: 'test-jwt-token' }))
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ data: 'ok' }),
    })
    vi.stubGlobal('fetch', mockFetch)

    await api.get('/test')
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/test'),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: 'Bearer test-jwt-token',
        }),
      }),
    )
  })

  it('does not attach header when no token', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ data: 'ok' }),
    })
    vi.stubGlobal('fetch', mockFetch)

    await api.get('/test')
    const callHeaders = mockFetch.mock.calls[0][1].headers
    expect(callHeaders.Authorization).toBeUndefined()
  })

  it('redirects to /login on 401', async () => {
    // Avoid actual redirect
    const originalHref = window.location.href
    Object.defineProperty(window, 'location', {
      value: {
        href: originalHref,
        pathname: '/history',
      },
      writable: true,
    })

    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: () => Promise.resolve({}),
    })
    vi.stubGlobal('fetch', mockFetch)

    await expect(api.get('/test')).rejects.toThrow(ApiError)
    expect(localStorage.getItem('auth')).toBeNull()
  })

  it('throws ApiError with status code on non-200/401', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve({ detail: 'Server error', code: 500 }),
    })
    vi.stubGlobal('fetch', mockFetch)

    await expect(api.get('/test')).rejects.toThrow(ApiError)
    try {
      await api.get('/test')
    } catch (e) {
      expect(e).toBeInstanceOf(ApiError)
      expect((e as ApiError).status).toBe(500)
      expect((e as ApiError).message).toBe('Server error')
    }
  })

  it('returns JSON on success', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ skills: [] }),
    })
    vi.stubGlobal('fetch', mockFetch)

    const result = await api.get('/skill/list')
    expect(result).toEqual({ skills: [] })
  })
})
