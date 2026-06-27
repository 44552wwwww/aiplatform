import { describe, it, expect, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import LoadingOverlay from '../LoadingOverlay.vue'

describe('LoadingOverlay', () => {
  afterEach(() => {
    document.body.innerHTML = ''
  })

  it('renders when visible is true', () => {
    mount(LoadingOverlay, { props: { visible: true } })
    expect(document.body.querySelector('.loading-overlay')).toBeTruthy()
  })

  it('does not render when visible is false', () => {
    mount(LoadingOverlay, { props: { visible: false } })
    expect(document.body.querySelector('.loading-overlay')).toBeFalsy()
  })

  it('shows custom message when provided', () => {
    mount(LoadingOverlay, { props: { visible: true, message: '处理中...' } })
    expect(document.body.querySelector('.loading-overlay__text')?.textContent).toBe('处理中...')
  })

  it('defaults visible to true', () => {
    mount(LoadingOverlay)
    expect(document.body.querySelector('.loading-overlay')).toBeTruthy()
  })
})
