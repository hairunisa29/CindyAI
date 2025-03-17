<template>
  <div
    :class="[
      'flex w-full gap-3',
      message.role === 'assistant' ? 'flex-row' : 'flex-row-reverse'
    ]"
  >
    <!-- Avatar -->
    <div class="flex-shrink-0">
      <div
        :class="[
          'flex h-8 w-8 items-center justify-center rounded-full',
          message.role === 'assistant' ? 'bg-primary text-primary-foreground' : 'bg-gray-200 text-gray-700'
        ]"
      >
        {{ message.role === 'assistant' ? 'AI' : 'U' }}
      </div>
    </div>

    <!-- Message Content -->
    <div
      :class="[
        'flex max-w-[80%] flex-col gap-1 rounded-[20px] px-4 py-2',
        message.role === 'assistant' 
          ? 'bg-white shadow-sm' 
          : 'bg-[#E5D4F8] text-gray-900'
      ]"
    >
      <!-- Message Text -->
      <div class="prose prose-sm max-w-none">
        {{ message.content }}
      </div>

      <!-- Sources -->
      <div 
        v-if="message.metadata?.sources?.length" 
        class="mt-2 text-xs text-gray-500"
      >
        <div class="font-medium">Sources:</div>
        <ul class="mt-1 list-disc pl-4">
          <li v-for="(source, index) in message.metadata.sources" :key="index">
            <a
              v-if="source.source_url"
              :href="source.source_url"
              target="_blank"
              rel="noopener noreferrer"
              class="text-primary hover:underline"
            >
              {{ source.title }}
            </a>
            <span v-else>{{ source.title }}</span>
          </li>
        </ul>
      </div>

      <!-- Timestamp -->
      <div 
        class="text-xs text-gray-400"
      >
        {{ formatDate(message.created_at) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage } from '../services/api'

defineProps<{
  message: ChatMessage
}>()

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script> 