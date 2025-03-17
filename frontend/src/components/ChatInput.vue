<template>
  <form @submit.prevent="handleSubmit" class="flex w-full items-end gap-2">
    <div class="relative flex-1">
      <textarea
        v-model="message"
        rows="1"
        placeholder="Type your message..."
        class="w-full resize-none rounded-full border bg-gray-50 px-6 py-3 pr-12 text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
        :class="{ 'opacity-50': isLoading }"
        @keydown.enter.prevent="handleEnter"
        @input="autoResize"
        ref="textarea"
      />
      <button
        type="submit"
        :disabled="isLoading || !message.trim()"
        class="absolute bottom-2 right-2 flex h-8 w-8 items-center justify-center rounded-full bg-primary text-white hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 20 20" 
          fill="currentColor" 
          class="h-5 w-5"
        >
          <path 
            d="M3.105 2.289a.75.75 0 00-.826.95l1.414 4.925A1.5 1.5 0 005.135 9.25h6.115a.75.75 0 010 1.5H5.135a1.5 1.5 0 00-1.442 1.086l-1.414 4.926a.75.75 0 00.826.95 28.896 28.896 0 0015.293-7.154.75.75 0 000-1.115A28.897 28.897 0 003.105 2.289z"
          />
        </svg>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{
  isLoading?: boolean
}>()

const emit = defineEmits<{
  (e: 'submit', message: string): void
}>()

const message = ref('')
const textarea = ref<HTMLTextAreaElement | null>(null)

function handleSubmit() {
  if (message.value.trim() && !props.isLoading) {
    emit('submit', message.value)
    message.value = ''
    if (textarea.value) {
      textarea.value.style.height = 'auto'
    }
  }
}

function handleEnter(e: KeyboardEvent) {
  if (e.shiftKey) {
    return
  }
  handleSubmit()
}

function autoResize() {
  if (textarea.value) {
    textarea.value.style.height = 'auto'
    textarea.value.style.height = textarea.value.scrollHeight + 'px'
  }
}

onMounted(() => {
  if (textarea.value) {
    textarea.value.focus()
  }
})
</script> 