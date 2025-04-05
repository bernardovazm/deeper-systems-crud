import { createRouter, createWebHistory } from 'vue-router'
import MainPage from './pages/MainPage.vue'
import UserPage from './pages/UserPage.vue'

const routes = [
  { path: '/', name: 'MainPage', component: MainPage },
  { path: '/user/:id', name: 'UserPage', component: UserPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
