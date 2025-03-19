import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Content {
  id: number
  title: string
  content_type: 'youtube' | 'article' | 'pdf'
  source_url?: string
  content_text?: string
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: number
  chat_id: number
  content_id?: number
  role: string
  content: string
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface Chat {
  id: number
  title?: string
  user_id: number
  created_at: string
  updated_at: string
  messages: ChatMessage[]
}

export interface ChatResponse {
  message: ChatMessage
  context?: string
  sources?: Record<string, any>[]
}

export const contentApi = {
  async createFromYoutube(videoUrl: string): Promise<Content> {
    const response = await api.post('/content/youtube', {
      video_url: videoUrl
    })
    return response.data
  },

  async getAll(): Promise<Content[]> {
    const response = await api.get('/content')
    return response.data
  },

  async get(id: number): Promise<Content> {
    const response = await api.get(`/content/${id}`)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/content/${id}`)
  },
}

export const chatApi = {
  async create(userId: number): Promise<Chat> {
    const response = await api.post('/chat', { user_id: userId })
    return response.data
  },

  async get(chatId: number): Promise<Chat> {
    const response = await api.get(`/chat/${chatId}`)
    return response.data
  },

  async getUserChats(userId: number): Promise<Chat[]> {
    const response = await api.get(`/chat/user/${userId}`)
    return response.data
  },

  async sendMessage(chatId: number, message: string, videoId?: string): Promise<ChatResponse> {
    const response = await api.post(`/chat/${chatId}/message`, {
      message: message,
      video_id: videoId
    })
    return response.data
  },
}

export default api 