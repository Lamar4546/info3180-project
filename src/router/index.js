// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '../views/HomeView.vue';
import AboutView from '../views/AboutView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import DashboardView from '../views/DashboardView.vue';
import EditProfileView from '../views/EditProfileView.vue';
import BrowseMatchesView from '../views/BrowseMatchesView.vue';
import MatchesView from '../views/MatchesView.vue';
import MessagesView from '../views/MessagesView.vue';
import ConversationView from '../views/ConversationView.vue';

/*
  Vue Router controls which page component appears for each URL.
  Each route below connects a browser path to one Vue view.
*/

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/profile/edit',
    name: 'edit-profile',
    component: EditProfileView
  },
  {
    path: '/browse',
    name: 'browse',
    component: BrowseMatchesView
  },
  {
    path: '/matches',
    name: 'matches',
    component: MatchesView
  },
  {
    path: '/messages',
    name: 'messages',
    component: MessagesView
  },
  {
    path: '/messages/:partnerId',
    name: 'conversation',
    component: ConversationView,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
