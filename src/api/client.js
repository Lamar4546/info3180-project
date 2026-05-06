// src/api/client.js

// Central place for all requests from Vue to the Flask backend.
const API_BASE_URL = 'http://localhost:5000';

/**
 * Helper for making API requests.
 */
 
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const config = {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  };

  const response = await fetch(url, config);

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(data?.error || data?.message || 'Something went wrong.');
  }

  return data;
}

// Authentication

// Registers a new user and creates their basic profile.
export function registerUser(formData) {
  return request('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(formData)
  });
}

// Logs in a user using their email and password.
export function loginUser(formData) {
  return request('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(formData)
  });
}

// Logs out the current user by clearing the Flask session.
export function logoutUser() {
  return request('/api/auth/logout', {
    method: 'POST'
  });
}

// Gets the currently logged-in user from the Flask session.
export function getCurrentUser() {
  return request('/api/auth/me');
}

// Profile

// Updates the logged-in user's profile information.
export function updateMyProfile(formData) {
  return request('/api/profiles/me', {
    method: 'PUT',
    body: JSON.stringify(formData)
  });
}

// Uploads a profile photo for the logged-in user.
export async function uploadProfilePhoto(photoFile) {
  const formData = new FormData();
  formData.append('photo', photoFile);

  const response = await fetch(`${API_BASE_URL}/api/profiles/me/photo`, {
    method: 'POST',
    credentials: 'include',
    body: formData
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(data?.error || 'Photo upload failed.');
  }

  return data;
}

// Gets all saved interests from the backend.
export function getInterests() {
  return request('/api/profiles/interests');
}

// Matches

// Gets browseable profiles using optional search/filter values.
export function browseMatches(filters = {}) {
  const query = new URLSearchParams(filters).toString();
  const endpoint = query ? `/api/matches/browse?${query}` : '/api/matches/browse';

  return request(endpoint);
}

// Sends a like or pass action for a selected profile.
export function sendMatchAction(profileId, action) {
  return request('/api/matches/action', {
    method: 'POST',
    body: JSON.stringify({
      profile_id: profileId,
      action
    })
  });
}

// Gets profiles where both users have liked each other.
export function getMatches() {
  return request('/api/matches');
}

// Messages

// Gets the current user's conversation list.
export function getConversations() {
  return request('/api/messages/conversations');
}

// Gets the message history with one matched user.
export function getMessageHistory(partnerId) {
  return request(`/api/messages/${partnerId}`);
}

// Sends a new message to a matched user.
export function sendMessage(receiverId, body) {
  return request('/api/messages/send', {
    method: 'POST',
    body: JSON.stringify({
      receiver_id: receiverId,
      body
    })
  });
}

// Converts a saved photo filename into a full Flask upload URL.
export function getPhotoUrl(filename) {
  return filename ? `${API_BASE_URL}/api/uploads/${filename}` : '';
}
