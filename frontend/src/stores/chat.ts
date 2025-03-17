import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Chat, ChatMessage, ChatResponse } from '../services/api'
import { chatApi } from '../services/api'

export const useChatStore = defineStore('chat', () => {
  const currentChat = ref<Chat | null>(null)
  const chats = ref<Chat[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const sortedMessages = computed(() => {
    if (!currentChat.value) return []
    // Sort messages by created_at timestamp
    return [...currentChat.value.messages].sort(
      (a, b) => {
        const timeA = new Date(a.created_at).getTime()
        const timeB = new Date(b.created_at).getTime()
        return timeA - timeB
      }
    )
  })

  async function createChat(userId: number) {
    try {
      loading.value = true
      error.value = null
      const chat = await chatApi.create(userId)
      chats.value.push(chat)
      currentChat.value = chat
      return chat
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create chat'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadChat(chatId: number) {
    try {
      loading.value = true
      error.value = null
      const chat = await chatApi.get(chatId)
      currentChat.value = chat
      return chat
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load chat'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadUserChats(userId: number) {
    try {
      loading.value = true
      error.value = null
      const userChats = await chatApi.getUserChats(userId)
      chats.value = userChats
      return userChats
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load chats'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function sendMessage(message: string): Promise<ChatResponse> {
    if (!currentChat.value) throw new Error('No active chat')
    
    try {
      loading.value = true
      error.value = null

      const userTimestamp = new Date().toISOString()
      
      // Add user message first with current timestamp
      if (currentChat.value) {
        currentChat.value.messages.push({
          id: Date.now(), // Temporary ID until refresh
          chat_id: currentChat.value.id,
          role: 'user',
          content: message,
          created_at: userTimestamp,
          updated_at: userTimestamp
        })
      }
      
      // Then get assistant's response
      const response = await chatApi.sendMessage(currentChat.value.id, message)
      
      // Add assistant response with a timestamp that's guaranteed to be after the user's message
      if (currentChat.value) {
        const assistantTimestamp = new Date(new Date(userTimestamp).getTime() + 1000).toISOString()
        currentChat.value.messages.push({
          ...response.message,
          created_at: assistantTimestamp,
          updated_at: assistantTimestamp
        })
      }
      
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to send message'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    currentChat,
    chats,
    loading,
    error,
    sortedMessages,
    createChat,
    loadChat,
    loadUserChats,
    sendMessage,
  }
}) 