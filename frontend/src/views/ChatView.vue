<template>
  <div class="flex h-screen flex-col bg-white">
    <!-- Header -->
    <header class="flex items-center justify-between border-b bg-white px-6 py-4">
      <div class="flex items-center gap-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <span class="text-lg font-semibold">AI</span>
        </div>
        <h1 class="text-xl font-semibold">Chat with Cindy</h1>
      </div>
      <!-- Only show Add Content button when not in iframe mode -->
      <button
        v-if="!route.params.contentId"
        @click="showContentModal = true"
        class="rounded-full bg-primary px-6 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
      >
        Add Learning Content
      </button>
    </header>

    <!-- Chat Messages -->
    <div class="flex-1 overflow-y-auto p-4" ref="messagesContainer">
      <div v-if="!chatStore.currentChat?.messages.length" class="flex flex-col items-center justify-center h-full text-center">
        <div class="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 mb-4">
          <span class="text-2xl">👋</span>
        </div>
        <h2 class="text-2xl font-semibold mb-2">Welcome to CindyAI</h2>
        <p class="text-muted-foreground max-w-md">
          I'm here to help you learn from your content. Start by adding some learning materials,
          then ask me questions about them!
        </p>
      </div>
      <template v-else>
        <ChatMessage
          v-for="message in chatStore.sortedMessages"
          :key="message.id"
          :message="message"
          class="mb-4"
        />
        <!-- Loading Message -->
        <div v-if="chatStore.loading" class="flex w-full gap-3">
          <div class="flex max-w-[80%] flex-col gap-1 rounded-[20px] bg-white px-4 py-2 shadow-sm">
            <div class="prose prose-sm max-w-none">
              I'm searching the content in this course to find the best answer for you.
            </div>
            <div class="flex items-center gap-1 mt-2">
              <div class="h-2 w-2 animate-bounce rounded-full bg-gray-300"></div>
              <div class="h-2 w-2 animate-bounce rounded-full bg-gray-300" style="animation-delay: 0.2s"></div>
              <div class="h-2 w-2 animate-bounce rounded-full bg-gray-300" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Chat Input -->
    <div class="border-t bg-white p-4">
      <ChatInput
        :is-loading="chatStore.loading"
        @submit="handleSendMessage"
        class="mx-auto max-w-3xl"
      />
    </div>

    <!-- Add Content Modal -->
    <div
      v-if="showContentModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm"
    >
      <div class="fixed left-[50%] top-[50%] z-50 w-full max-w-lg translate-x-[-50%] translate-y-[-50%] rounded-[20px] border bg-white p-6 shadow-lg">
        <h2 class="text-lg font-semibold mb-4">Add Learning Content</h2>
        
        <div class="space-y-4">
          <div>
            <label class="text-sm font-medium">YouTube Video URL</label>
            <input
              v-model="youtubeUrl"
              type="text"
              placeholder="https://www.youtube.com/watch?v=..."
              class="mt-1 w-full rounded-full border bg-gray-50 px-4 py-2 text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          </div>
          
          <div class="flex justify-end gap-2">
            <button
              @click="showContentModal = false"
              class="rounded-full border px-6 py-2 text-sm hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              @click="handleAddContent"
              :disabled="contentStore.loading"
              class="rounded-full bg-primary px-6 py-2 text-sm text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
            >
              {{ contentStore.loading ? 'Adding...' : 'Add Content' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useChatStore } from '../stores/chat'
import { useContentStore } from '../stores/content'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'

const route = useRoute()
const chatStore = useChatStore()
const contentStore = useContentStore()

const showContentModal = ref(false)
const youtubeUrl = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// Initialize chat and load content if contentId is provided
onMounted(async () => {
  try {
    // Create chat for user ID 1 (in a real app, this would come from authentication)
    if (!chatStore.currentChat) {
      await chatStore.createChat(1)
    }

    // If contentId is provided in the URL, load the content
    const contentId = route.params.contentId
    if (contentId) {
      if (isNaN(Number(contentId))) {
        // If contentId is not a number, treat it as a YouTube video ID
        // Force a fresh load with youtu.be URL format
        await contentStore.addYoutubeContent(`https://youtu.be/${contentId}`)
      } else {
        // If it's a number, load from database as before
        await contentStore.loadContent(Number(contentId))
      }
    }
  } catch (error) {
    console.error('Failed to initialize chat:', error)
  }
})

// Watch for changes in the route params
watch(() => route.params.contentId, async (newContentId) => {
  if (newContentId) {
    try {
      if (isNaN(Number(newContentId))) {
        // If newContentId is not a number, treat it as a YouTube video ID
        // Force a fresh load with youtu.be URL format
        await contentStore.addYoutubeContent(`https://youtu.be/${newContentId}`)
      } else {
        // If it's a number, load from database as before
        await contentStore.loadContent(Number(newContentId))
      }
    } catch (error) {
      console.error('Failed to load content:', error)
    }
  }
}, { immediate: false })

// Scroll to bottom when new messages arrive
watch(() => chatStore.currentChat?.messages.length, async () => {
  await nextTick()
  scrollToBottom()
})

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

async function handleSendMessage(message: string) {
  try {
    const videoId = route.params.contentId as string;
    
    await chatStore.sendMessage(message, videoId)
  } catch (error) {
    console.error('Failed to send message:', error)
    // TODO: Show error toast
  }
}

async function handleAddContent() {
  if (!youtubeUrl.value) return

  try {
    const content = await contentStore.addYoutubeContent(youtubeUrl.value)
    showContentModal.value = false
    youtubeUrl.value = ''
    // TODO: Show success toast
  } catch (error) {
    console.error('Failed to add content:', error)
    // TODO: Show error toast
  }
}
</script> 