<template>
  <form class="match-filters" @submit.prevent="applyFilters">
    <div class="row g-3">
      <div class="col-md-4">
        <label for="search" class="form-label">Search</label>
        <input
          id="search"
          v-model.trim="localFilters.search"
          type="text"
          class="form-control"
          placeholder="Name or bio keyword"
        />
      </div>

      <div class="col-md-4">
        <label for="parish" class="form-label">Location / Parish</label>
        <input
          id="parish"
          v-model.trim="localFilters.parish"
          type="text"
          class="form-control"
          placeholder="Kingstown, Calliaqua, etc."
        />
      </div>

      <div class="col-md-4">
        <label for="interest" class="form-label">Interest</label>
        <input
          id="interest"
          v-model.trim="localFilters.interest"
          type="text"
          class="form-control"
          placeholder="music, football, food..."
        />
      </div>

      <div class="col-md-3">
        <label for="ageMin" class="form-label">Min Age</label>
        <input
          id="ageMin"
          v-model.number="localFilters.age_min"
          type="number"
          min="18"
          max="99"
          class="form-control"
        />
      </div>

      <div class="col-md-3">
        <label for="ageMax" class="form-label">Max Age</label>
        <input
          id="ageMax"
          v-model.number="localFilters.age_max"
          type="number"
          min="18"
          max="99"
          class="form-control"
        />
      </div>

      <div class="col-md-6 d-flex align-items-end gap-2">
        <button type="submit" class="btn btn-primary flex-fill">
          Apply Filters
        </button>

        <button
          type="button"
          class="btn btn-outline-secondary flex-fill"
          @click="clearFilters"
        >
          Clear
        </button>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  name: 'MatchFilters',

  emits: ['filter', 'clear'],

  data() {
    return {
      // These values are edited locally before being sent to the Browse page.
      localFilters: {
        search: '',
        parish: '',
        interest: '',
        age_min: 18,
        age_max: 99
      }
    };
  },

  methods: {
    /*
      Sends the current filter values to the parent page.
      Empty text fields are removed so the API query stays clean.
    */
    applyFilters() {
      const filters = {};

      Object.entries(this.localFilters).forEach(([key, value]) => {
        if (value !== '' && value !== null && value !== undefined) {
          filters[key] = value;
        }
      });

      this.$emit('filter', filters);
    },

    /*
      Resets the filter form and tells the parent page to reload
      the default browse results.
    */
    clearFilters() {
      this.localFilters = {
        search: '',
        parish: '',
        interest: '',
        age_min: 18,
        age_max: 99
      };

      this.$emit('clear');
    }
  }
};
</script>
