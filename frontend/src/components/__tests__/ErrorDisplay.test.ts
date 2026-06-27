import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ErrorDisplay from '../ErrorDisplay.vue'

describe('ErrorDisplay', () => {
  it('renders error message', () => {
    const wrapper = mount(ErrorDisplay, {
      props: { error: '网络连接失败' },
    })
    expect(wrapper.find('.error-display__message').text()).toBe('网络连接失败')
  })

  it('renders nothing when error is null', () => {
    const wrapper = mount(ErrorDisplay, { props: { error: null } })
    expect(wrapper.find('.error-display').exists()).toBe(false)
  })

  it('shows retry button when retry callback provided', () => {
    const retry = vi.fn()
    const wrapper = mount(ErrorDisplay, {
      props: { error: '出错了', retry },
    })
    expect(wrapper.find('.error-display__retry').exists()).toBe(true)
  })

  it('calls retry function on button click', async () => {
    const retry = vi.fn()
    const wrapper = mount(ErrorDisplay, {
      props: { error: '出错了', retry },
    })
    await wrapper.find('.error-display__retry').trigger('click')
    expect(retry).toHaveBeenCalledOnce()
  })

  it('does not show retry button when retry is not provided', () => {
    const wrapper = mount(ErrorDisplay, {
      props: { error: '出错了' },
    })
    expect(wrapper.find('.error-display__retry').exists()).toBe(false)
  })
})
