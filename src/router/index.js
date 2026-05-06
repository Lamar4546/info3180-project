// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import { getCurrentUser } from '../api/client';

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
  meta.requiresAuth marks pages that should only be viewed after login.
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
    component: DashboardView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/profile/edit',
    name: 'edit-profile',
    component: EditProfileView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/browse',
    name: 'browse',
    component: BrowseMatchesView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/matches',
    name: 'matches',
    component: MatchesView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/messages',
    name: 'messages',
    component: MessagesView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/messages/:partnerId',
    name: 'conversation',
    component: ConversationView,
    props: true,
    meta: {
      requiresAuth: true
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

/*
  Global route guard.

  Before opening a protected route, Vue checks with Flask to see
  whether a user is currently logged in.
*/
router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) {
    return true;
  }

  try {
    await getCurrentUser();
    return true;
  } catch {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath
      }
    };
  }
});

export default router;
