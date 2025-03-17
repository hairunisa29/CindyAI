import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Content } from '../services/api'
import { contentApi } from '../services/api'

export const useContentStore = defineStore('content', () => {
  const contents = ref<Content[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  function clearContents() {
    contents.value = []
  }

  async function loadContents() {
    try {
      loading.value = true
      error.value = null
      const data = await contentApi.getAll()
      contents.value = data
      return data
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load contents'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function loadContent(contentId: number) {
    try {
      loading.value = true
      error.value = null
      const content = await contentApi.get(contentId)
      if (!contents.value.find(c => c.id === content.id)) {
        contents.value.push(content)
      }
      return content
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load content'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function getVideoIdFromUrl(url: string): Promise<string> {
    const match = url.match(/[?&]v=([^&]+)/);
    return match ? match[1] : url;
  }

  async function addYoutubeContent(videoUrl: string) {
    try {
      loading.value = true
      error.value = null
      
      // Create new content directly without checking existing content
      const content = await contentApi.createFromYoutube(videoUrl)
      
      // Replace all contents with just this one
      contents.value = [content]
      return content
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to add YouTube content'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteContent(contentId: number) {
    try {
      loading.value = true
      error.value = null
      await contentApi.delete(contentId)
      contents.value = contents.value.filter(c => c.id !== contentId)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete content'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    contents,
    loading,
    error,
    clearContents,
    loadContents,
    loadContent,
    addYoutubeContent,
    deleteContent,
  }
}) 