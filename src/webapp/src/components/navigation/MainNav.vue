<script>
import { mapGetters, mapState } from 'vuex'

import capitalize from '@/filters/capitalize'
import underscoreToSpace from '@/filters/underscoreToSpace'
import utils from '@/utils/utils'

import Dropdown from '@/components/generic/Dropdown'
import Logo from '@/components/navigation/Logo'

export default {
  name: 'MainNav',
  components: {
    Dropdown,
    Logo
  },
  filters: {
    capitalize,
    underscoreToSpace
  },
  data() {
    return {
      isMobileMenuOpen: false
    }
  },
  computed: {
    ...mapGetters('configuration', ['getRunningPipelines']),
    ...mapGetters('repos', ['hasModels', 'urlForModelDesign']),
    ...mapGetters('system', ['updateAvailable']),
    ...mapGetters('plugins', [
      'getIsStepLoadersMinimallyValidated',
      'getIsStepTransformsMinimallyValidated',
      'getIsStepScheduleMinimallyValidated'
    ]),
    ...mapState('repos', ['models']),
    ...mapState('system', ['latestVersion', 'updating', 'version']),
    getIconColor() {
      return parentPath =>
        this.getIsSubRouteOf(parentPath)
          ? 'has-text-interactive-navigation'
          : 'has-text-grey-light'
    },
    getIsCurrentPath() {
      return path => this.$route.path.includes(path)
    },
    getIsSubRouteOf() {
      return parentPath => utils.getIsSubRouteOf(parentPath, this.$route.path)
    }
  },
  watch: {
    $route() {
      if (this.isMobileMenuOpen) {
        this.closeMobileMenu()
      }
    }
  },
  created() {
    this.$store.dispatch('repos/getModels')
  },
  methods: {
    closeMobileMenu() {
      this.isMobileMenuOpen = false
    },
    goToSchedules() {
      this.$router.push({ name: 'schedules' })
    },
    mobileMenuClicked() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen
    },
    startUpgrade() {
      this.$store.dispatch('system/upgrade').then(() => {
        document.location.reload()
      })
    }
  }
}
</script>

<template>
  <nav class="navbar is-transparent">
    <div class="navbar-brand">
      <div class="navbar-item navbar-child">
        <Logo />
        <span
          class="meltano-label is-uppercase has-text-weight-bold has-text-primary ml-05r"
          >Meltano</span
        >
      </div>
      <div
        class="navbar-burger burger"
        :class="{ 'is-active': isMobileMenuOpen }"
        data-target="meltnavbar-transparent"
        @click="mobileMenuClicked"
      >
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>

    <div
      id="meltnavbar-transparent"
      class="navbar-menu"
      :class="{ 'is-active': isMobileMenuOpen }"
    >
      <div class="navbar-start">
        <div class="navbar-item navbar-child has-dropdown is-hoverable">
          <router-link
            :to="{ name: 'dataSetup' }"
            :class="{ 'router-link-active': getIsSubRouteOf('/pipeline') }"
            class="navbar-link has-text-weight-semibold"
          >
            <a
              class="button has-background-transparent is-borderless is-paddingless"
              :class="{
                'has-text-interactive-navigation': getIsSubRouteOf('/pipeline')
              }"
            >
              <span class="icon is-small" :class="getIconColor('/pipeline')">
                <font-awesome-icon icon="stream"></font-awesome-icon>
              </span>
              <span>Pipelines</span>
              <span
                v-if="getRunningPipelines.length > 0"
                class="tag tag-running-pipelines is-rounded is-info"
                @click.prevent="goToSchedules"
              >
                {{ getRunningPipelines.length }}
              </span>
            </a>
          </router-link>

          <div class="navbar-dropdown">
            <router-link
              :to="{ name: 'extractors' }"
              class="navbar-item button is-borderless"
              :class="{
                'is-active': getIsCurrentPath('/pipeline/extract')
              }"
              tag="button"
              >Extract</router-link
            >
            <router-link
              :to="{ name: 'loaders' }"
              class="navbar-item button is-borderless"
              :class="{ 'is-active': getIsCurrentPath('/pipeline/load') }"
              :disabled="!getIsStepLoadersMinimallyValidated"
              tag="button"
              >Load</router-link
            >
            <router-link
              :to="{ name: 'transforms' }"
              class="navbar-item button is-borderless"
              :class="{
                'is-active': getIsCurrentPath('/pipeline/transform')
              }"
              :disabled="!getIsStepTransformsMinimallyValidated"
              tag="button"
              >Transform</router-link
            >
            <router-link
              :to="{ name: 'schedules' }"
              class="navbar-item button is-borderless"
              :class="{ 'is-active': getIsCurrentPath('/pipeline/schedule') }"
              :disabled="!getIsStepScheduleMinimallyValidated"
              tag="button"
              >Schedule</router-link
            >
          </div>
        </div>

        <router-link
          :to="{ name: 'orchestration' }"
          :class="{ 'router-link-active': getIsSubRouteOf('/orchestrate') }"
          class="navbar-item navbar-child has-text-weight-semibold"
        >
          <a
            class="button has-background-transparent is-borderless is-paddingless"
            :class="{
              'has-text-interactive-navigation': getIsSubRouteOf('/orchestrate')
            }"
          >
            <span class="icon is-small" :class="getIconColor('/orchestrate')">
              <font-awesome-icon icon="project-diagram"></font-awesome-icon>
            </span>
            <span>Orchestrate</span>
          </a>
        </router-link>

        <router-link
          :to="{ name: 'model' }"
          :class="{ 'router-link-active': getIsSubRouteOf('/model') }"
          class="navbar-item navbar-child has-text-weight-semibold"
        >
          <a
            class="button has-background-transparent is-borderless is-paddingless"
            :class="{
              'has-text-interactive-navigation': getIsSubRouteOf('/model')
            }"
          >
            <span class="icon is-small" :class="getIconColor('/model')">
              <font-awesome-icon icon="file-alt"></font-awesome-icon>
            </span>
            <span>Model</span>
          </a>
        </router-link>

        <div class="navbar-item navbar-child has-dropdown is-hoverable">
          <a
            :class="{ 'router-link-active': getIsSubRouteOf('/analyze') }"
            class="navbar-link has-text-weight-semibold"
          >
            <a
              class="button has-background-transparent is-borderless is-paddingless"
              :class="{
                'has-text-interactive-navigation': getIsSubRouteOf('/analyze')
              }"
            >
              <span class="icon is-small" :class="getIconColor('/analyze')">
                <font-awesome-icon icon="chart-line"></font-awesome-icon>
              </span>
              <span>Analyze</span>
            </a>
          </a>

          <div class="navbar-dropdown">
            <template v-if="hasModels">
              <div
                v-for="(v, model) in models"
                :key="`${model}-panel`"
                class="box box-analyze-nav is-borderless is-shadowless is-marginless"
              >
                <div class="content">
                  <h3 class="is-size-6">
                    {{ v.name | capitalize | underscoreToSpace }}
                  </h3>
                  <h4 class="is-size-7 has-text-grey">
                    {{ v.namespace }}
                  </h4>
                </div>
                <div class="buttons">
                  <router-link
                    v-for="design in v['designs']"
                    :key="design"
                    class="button is-small is-interactive-primary is-outlined"
                    :to="urlForModelDesign(model, design)"
                    >{{ design | capitalize | underscoreToSpace }}</router-link
                  >
                </div>
              </div>
            </template>
            <template v-else>
              <div class="box is-borderless is-shadowless is-marginless">
                <div class="content">
                  <h3 class="is-size-6">
                    No Models Installed
                  </h3>
                  <p>
                    Models are inferred and automatically installed for you
                    based off the installed Extractors from your data pipelines.
                    Set up a pipeline first.
                  </p>
                  <router-link
                    class="button is-interactive-primary"
                    :to="{ name: 'dataSetup' }"
                    >Create Data Pipeline</router-link
                  >
                </div>
              </div>
            </template>
          </div>
        </div>

        <router-link
          :to="{ name: 'dashboards' }"
          :class="{ 'router-link-active': getIsSubRouteOf('/dashboard') }"
          class="navbar-item navbar-child has-text-weight-semibold"
        >
          <a
            class="button has-background-transparent is-borderless is-paddingless"
            :class="{
              'has-text-interactive-navigation': getIsSubRouteOf('/dashboard')
            }"
          >
            <span class="icon is-small" :class="getIconColor('/dashboard')">
              <font-awesome-icon icon="th-large"></font-awesome-icon>
            </span>
            <span>Dashboard</span>
          </a>
        </router-link>

        <a
          class="navbar-item navbar-child has-text-weight-semibold"
          target="_blank"
          href="https://www.meltano.com/tutorials/using-jupyter-notebooks.html#using-jupyter-notebooks"
        >
          <a
            class="button has-background-transparent is-borderless is-paddingless"
            :class="{
              'has-text-interactive-navigation': getIsSubRouteOf('/notebook')
            }"
          >
            <span class="icon is-small" :class="getIconColor('/notebook')">
              <font-awesome-icon icon="book-open"></font-awesome-icon>
            </span>
            <span>Notebook</span>
          </a>
        </a>
      </div>

      <div class="navbar-end">
        <div class="navbar-item navbar-child level">
          <div class="level-right">
            <div v-if="updateAvailable" class="level-item">
              <Dropdown
                label="Update Available"
                :button-classes="
                  `is-info is-small ${updating ? 'is-loading' : ''}`
                "
                menu-classes="dropdown-menu-600"
                icon-open="gift"
                icon-close="caret-up"
                is-right-aligned
              >
                <div class="dropdown-content is-unselectable">
                  <div class="dropdown-item">
                    <p>
                      View the
                      <a
                        href="https://gitlab.com/meltano/meltano/blob/master/CHANGELOG.md"
                        target="_blank"
                        >CHANGELOG.md</a
                      >
                      to see what is updated by the version.
                    </p>
                    <p class="is-italic">
                      This information will be inlined here in the future via
                      <a
                        href="https://gitlab.com/meltano/meltano/issues/961"
                        target="_blank"
                        >#961</a
                      >
                    </p>
                  </div>
                  <div class="dropdown-item">
                    <div class="level">
                      <div class="level-left">
                        <div class="field is-grouped is-grouped-multiline">
                          <div class="control">
                            <div class="tags has-addons">
                              <span class="tag">Current</span>
                              <span class="tag is-info">{{ version }}</span>
                            </div>
                          </div>
                          <div class="control">
                            <div class="tags has-addons">
                              <span class="tag">Latest</span>
                              <span class="tag is-info">{{
                                latestVersion
                              }}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="level-right">
                        <div class="buttons is-right">
                          <button
                            class="button is-text"
                            data-dropdown-auto-close
                          >
                            Cancel
                          </button>
                          <button
                            class="button is-interactive-primary"
                            data-dropdown-auto-close
                            @click="startUpgrade"
                          >
                            Update Meltano
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Dropdown>
            </div>
            <div class="level-item">
              <a
                class="button"
                target="_blank"
                href="https://meltano.com/docs/getting-help.html"
              >
                <span class="icon">
                  <font-awesome-icon icon="question-circle"></font-awesome-icon>
                </span>
                <span>Help</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style lang="scss">
@import '@/scss/bulma-preset-overrides.scss';

.box-analyze-nav {
  min-width: 240px;
}

.meltano-label {
  @media screen and (min-width: $tablet) {
    display: none;
  }
}
.navbar-menu {
  background-color: transparent;
}
.navbar-burger span {
  color: $interactive-navigation;
}
.navbar-brand .navbar-item {
  padding: 0 1rem;
}
.navbar.is-transparent {
  background-color: transparent;

  .navbar-start .navbar-link,
  .navbar-start > .navbar-item {
    color: $interactive-navigation-inactive;
    border-bottom: 1px solid $grey-lighter;

    &.router-link-active {
      color: $interactive-navigation;
      border-color: $interactive-navigation;
    }
  }
  .navbar-item {
    &.has-dropdown {
      border-bottom: none;
    }
  }

  .navbar-start .navbar-link::after {
    border-color: $interactive-navigation-inactive;
  }
  .navbar-start .navbar-link:hover::after {
    border-color: $interactive-navigation;
  }

  .navbar-brand > a.navbar-item:hover,
  .navbar-start > a.navbar-item.is-active,
  .navbar-start > a.navbar-item:hover {
    background: transparent;
    color: $interactive-navigation;
    border-bottom: 1px solid $interactive-navigation-inactive;
  }
}
.tag-running-pipelines {
  margin-left: 0.5rem;
}
</style>
