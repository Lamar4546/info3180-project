<template>
  <main class="page-section">
    <div class="container">
      <div class="page-card profile-edit-card">
        <div class="profile-edit-header">
          <div>
            <p class="dashboard-kicker text-primary">Profile Settings</p>
            <h1>Edit Your Profile</h1>
            <p>
              Keep your profile updated so DriftDater can suggest better matches.
            </p>
          </div>
        </div>

        <AlertMessage :message="errorMessage" type="error" />
        <AlertMessage :message="successMessage" type="success" />

        <LoadingSpinner
          v-if="isLoadingProfile"
          message="Loading your profile..."
        />

        <form v-else @submit.prevent="handleUpdateProfile">
          <section class="profile-photo-section mb-4">
            <div class="profile-photo-preview">
              <img
                v-if="photoPreview"
                :src="photoPreview"
                alt="Profile preview"
              />
              <span v-else>👤</span>
            </div>

            <div class="flex-grow-1">
              <label for="photo" class="form-label">Profile Photo</label>
              <input
                id="photo"
                type="file"
                class="form-control"
                accept="image/png, image/jpeg, image/jpg, image/gif, image/webp"
                @change="handlePhotoSelection"
              />

              <button
                type="button"
                class="btn btn-outline-primary mt-2"
                :disabled="!selectedPhoto || isUploadingPhoto"
                @click="handlePhotoUpload"
              >
                {{ isUploadingPhoto ? 'Uploading...' : 'Upload Photo' }}
              </button>

              <small class="text-muted d-block mt-2">
                Accepted formats: PNG, JPG, JPEG, GIF, or WEBP.
              </small>
            </div>
          </section>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="firstName" class="form-label">First Name</label>
              <input
                id="firstName"
                v-model.trim="form.first_name"
                type="text"
                class="form-control"
                required
              />
            </div>

            <div class="col-md-6 mb-3">
              <label for="lastName" class="form-label">Last Name</label>
              <input
                id="lastName"
                v-model.trim="form.last_name"
                type="text"
                class="form-control"
                required
              />
            </div>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="gender" class="form-label">Gender</label>
              <select
                id="gender"
                v-model="form.gender"
                class="form-select"
                required
              >
                <option value="">Select gender</option>
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="col-md-6 mb-3">
              <label for="lookingFor" class="form-label">Looking For</label>
              <select
                id="lookingFor"
                v-model="form.looking_for"
                class="form-select"
              >
                <option value="Any">Any</option>
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <div class="mb-3">
            <label for="parish" class="form-label">Location / Parish</label>
            <input
              id="parish"
              v-model.trim="form.parish"
              type="text"
              class="form-control"
              placeholder="Kingstown, Calliaqua, etc."
            />
          </div>

          <div class="mb-3">
            <label for="bio" class="form-label">Bio</label>
            <textarea
              id="bio"
              v-model.trim="form.bio"
              class="form-control"
              rows="4"
              placeholder="Tell people a little about yourself..."
            ></textarea>
          </div>

          <div class="mb-3">
            <label for="interests" class="form-label">Interests</label>
            <input
              id="interests"
              v-model.trim="interestsText"
              type="text"
              class="form-control"
              placeholder="music, football, food, hiking"
            />
            <small class="text-muted">
              Enter at least 3 interests, separated by commas.
            </small>
          </div>

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="ageMin" class="form-label">Minimum Preferred Age</label>
              <input
                id="ageMin"
                v-model.number="form.age_min"
                type="number"
                min="18"
                max="99"
                class="form-control"
              />
            </div>

            <div class="col-md-6 mb-3">
              <label for="ageMax" class="form-label">Maximum Preferred Age</label>
              <input
                id="ageMax"
                v-model.number="form.age_max"
                type="number"
                min="18"
                max="99"
                class="form-control"
              />
            </div>
          </div>

          <div class="form-check form-switch mb-4">
            <input
              id="isPublic"
              v-model="form.is_public"
              class="form-check-input"
              type="checkbox"
            />
            <label for="isPublic" class="form-check-label">
              Make my profile public
            </label>
          </div>

          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="isSaving"
          >
            {{ isSaving ? 'Saving profile...' : 'Save Profile' }}
          </button>
        </form>
      </div>
    </div>
  </main>
</template>

<script>
import {
  getCurrentUser,
  updateMyProfile,
  uploadProfilePhoto,
  getPhotoUrl
} from '../api/client';
import AlertMessage from '../components/AlertMessage.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
  name: 'EditProfileView',

  components: {
    AlertMessage,
    LoadingSpinner
  },

  data() {
    return {
      // Stores editable profile fields before sending them to Flask.
      form: {
        first_name: '',
        last_name: '',
        gender: '',
        looking_for: 'Any',
        parish: '',
        bio: '',
        age_min: 18,
        age_max: 99,
        is_public: true
      },

      // Interests are typed as comma-separated text, then converted to an array.
      interestsText: '',

      // Photo upload state.
      selectedPhoto: null,
      photoPreview: '',

      // Loading and feedback states.
      isLoadingProfile: true,
      isSaving: false,
      isUploadingPhoto: false,
      errorMessage: '',
      successMessage: ''
    };
  },

  async mounted() {
    await this.loadProfile();
  },

  methods: {
    /*
      loadProfile()

      Gets the logged-in user's profile from Flask and fills the form.
      This lets the user edit their existing profile instead of starting blank.
    */
    async loadProfile() {
      this.errorMessage = '';
      this.successMessage = '';

      try {
        this.isLoadingProfile = true;

        const user = await getCurrentUser();
        const profile = user.profile;

        if (!profile) {
          this.errorMessage = 'No profile was found for this user.';
          return;
        }

        this.form = {
          first_name: profile.first_name || '',
          last_name: profile.last_name || '',
          gender: profile.gender || '',
          looking_for: profile.looking_for || 'Any',
          parish: profile.parish || '',
          bio: profile.bio || '',
          age_min: profile.age_min || 18,
          age_max: profile.age_max || 99,
          is_public: profile.is_public ?? true
        };

        this.interestsText = profile.interests ? profile.interests.join(', ') : '';
        this.photoPreview = profile.photo ? getPhotoUrl(profile.photo) : '';
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoadingProfile = false;
      }
    },

    /*
      handlePhotoSelection()

      Stores the selected image and creates a temporary preview before upload.
    */
    handlePhotoSelection(event) {
      const file = event.target.files[0];

      if (!file) {
        this.selectedPhoto = null;
        return;
      }

      this.selectedPhoto = file;
      this.photoPreview = URL.createObjectURL(file);
    },

    /*
      handlePhotoUpload()

      Sends the selected photo to the Flask photo upload endpoint.
    */
    async handlePhotoUpload() {
      this.errorMessage = '';
      this.successMessage = '';

      if (!this.selectedPhoto) {
        this.errorMessage = 'Please select a photo first.';
        return;
      }

      try {
        this.isUploadingPhoto = true;

        const result = await uploadProfilePhoto(this.selectedPhoto);

        this.photoPreview = getPhotoUrl(result.photo);
        this.successMessage = 'Profile photo uploaded successfully.';
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isUploadingPhoto = false;
      }
    },

    /*
      handleUpdateProfile()

      Converts interests into an array, validates age preferences,
      and sends updated profile details to Flask.
    */
    async handleUpdateProfile() {
      this.errorMessage = '';
      this.successMessage = '';

      const interests = this.interestsText
        .split(',')
        .map((interest) => interest.trim().toLowerCase())
        .filter((interest) => interest.length > 0);

      if (interests.length < 3) {
        this.errorMessage = 'Please enter at least 3 interests.';
        return;
      }

      if (this.form.age_min > this.form.age_max) {
        this.errorMessage = 'Minimum age cannot be greater than maximum age.';
        return;
      }

      try {
        this.isSaving = true;

        await updateMyProfile({
          ...this.form,
          interests
        });

        this.successMessage = 'Profile updated successfully.';
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isSaving = false;
      }
    }
  }
};
</script>
