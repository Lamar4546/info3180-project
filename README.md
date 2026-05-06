## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Start Flask API

Remember to always create a virtual environment and install the packages in your requirements file

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
$ flask --app app --debug run
```

## Frontend Lead Contribution

The Frontend Lead was responsible for building and organizing the Vue 3 user interface for DriftDater. This included page routing, reusable components, authentication screens, profile editing screens, match browsing, messaging views, responsive styling, and integration with the Flask API.

### Main Frontend Responsibilities

- Set up Vue Router navigation for all major pages.
- Created reusable Vue components for alerts, loading states, profile cards, and match filters.
- Built the login and registration pages with form validation and user feedback.
- Connected authentication forms to the Flask backend API.
- Built the dashboard page with quick actions for profile editing, browsing, matches, and messages.
- Built the edit profile page with profile photo upload support.
- Built the browse matches page with filtering and like/pass actions.
- Built the mutual matches page.
- Built the messages and conversation views.
- Added route guards to protect pages that require login.
- Updated the DriftDater logo, browser title, favicon, and frontend styling.
- Improved the interface with responsive layouts and consistent UI styling.

### Main Frontend Files

```text
src/api/client.js
src/router/index.js
src/App.vue
src/components/AppHeader.vue
src/components/AppFooter.vue
src/components/AlertMessage.vue
src/components/LoadingSpinner.vue
src/components/ProfileCard.vue
src/components/MatchFilters.vue
src/views/HomeView.vue
src/views/AboutView.vue
src/views/LoginView.vue
src/views/RegisterView.vue
src/views/DashboardView.vue
src/views/EditProfileView.vue
src/views/BrowseMatchesView.vue
src/views/MatchesView.vue
src/views/MessagesView.vue
src/views/ConversationView.vue
src/assets/base.css
