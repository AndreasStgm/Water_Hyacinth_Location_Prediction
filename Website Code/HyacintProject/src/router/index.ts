import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HartbeespoortDamView from "@/views/HartbeespoortDamView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/hartbeespoortDam',
      name: 'hartbeespoortDam',
      component: HartbeespoortDamView
    }
  ]
})

export default router
