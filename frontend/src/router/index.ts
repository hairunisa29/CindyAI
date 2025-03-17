import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '../views/ChatView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/chat/:contentId',
      name: 'chat-with-content',
      component: ChatView,
      props: true
    }
  ]
})

export default router 