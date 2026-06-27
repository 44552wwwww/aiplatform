import { api } from './client'

export interface LoginParams {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: {
    id: number
    username: string
  }
}

export interface UserInfo {
  id: number
  username: string
}

export const authApi = {
  register(data: LoginParams) {
    return api.post<TokenResponse>('/auth/register', data)
  },

  login(data: LoginParams) {
    return api.post<TokenResponse>('/auth/login', data)
  },

  me() {
    return api.get<UserInfo>('/auth/me')
  },
}
