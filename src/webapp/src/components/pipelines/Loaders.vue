<script>
import { mapGetters, mapState } from 'vuex'

import ConnectorLogo from '@/components/generic/ConnectorLogo'
import SpeedRunIcon from '@/components/pipelines/SpeedRunIcon'

export default {
  name: 'Loaders',
  components: {
    ConnectorLogo,
    SpeedRunIcon
  },
  data: () => ({
    speedRunLoader: 'target-sqlite'
  }),
  computed: {
    ...mapGetters('plugins', [
      'getIsAddingPlugin',
      'getIsInstallingPlugin',
      'getIsPluginInstalled'
    ]),
    ...mapState('plugins', ['plugins']),
    sortedLoaders() {
      // This is a stop gap until we implement an eventual need for automatic text filtering for cards
      const currentLoaders = this.plugins.loaders || []
      let orderedForSpeedRunLoaders = []

      if (currentLoaders.length > 0) {
        const start = [
          currentLoaders.find(plugin => plugin.name === this.speedRunLoader)
        ]
        const end = currentLoaders.filter(
          plugin => plugin.name !== this.speedRunLoader
        )
        orderedForSpeedRunLoaders = start.concat(end)
      }

      return orderedForSpeedRunLoaders
    }
  },
  methods: {
    updateLoaderSettings(loader) {
      this.$router.push({ name: 'loaderSettings', params: { loader } })
    }
  }
}
</script>

<template>
  <div>
    <div class="columns">
      <div class="column is-three-fifths is-offset-one-fifth">
        <div class="content has-text-centered">
          <p class="level-item buttons">
            <a class="button is-small is-static is-marginless is-borderless">
              <span>Tell us which loader(s) to install</span>
            </a>
            <span class="step-spacer">then</span>
            <a class="button is-small is-static is-marginless is-borderless">
              <span>Configure and save their settings</span>
            </a>
          </p>
        </div>
      </div>
    </div>

    <div class="tile is-ancestor is-flex is-flex-wrap">
      <div
        v-for="(loader, index) in sortedLoaders"
        :key="`${loader.name}-${index}`"
        :data-test-id="`${loader.name}-loader-card`"
        class="tile is-parent is-3 is-relative"
      >
        <div class="tile level is-child box">
          <SpeedRunIcon v-if="loader.name === speedRunLoader" />
          <div class="image level-item is-64x64 container">
            <ConnectorLogo
              :connector="loader.name"
              :is-grayscale="!getIsPluginInstalled('loaders', loader.name)"
            />
          </div>
          <div class="content is-small">
            <p class="has-text-centered has-text-weight-semibold">
              {{ loader.name }}
            </p>
            <p class="has-text-centered">
              {{ loader.description }}
            </p>

            <a
              v-if="getIsPluginInstalled('loaders', loader.name)"
              class="button is-interactive-primary is-block is-small"
              @click="updateLoaderSettings(loader.name)"
              >Configure</a
            >
            <a
              v-else
              :class="{
                'is-loading':
                  getIsAddingPlugin('loaders', loader.name) ||
                  getIsInstallingPlugin('loaders', loader.name)
              }"
              class="button is-interactive-primary is-outlined is-block is-small"
              @click="updateLoaderSettings(loader.name)"
              >Install</a
            >
          </div>
        </div>
      </div>
    </div>
    <progress
      v-if="!plugins.loaders"
      class="progress is-small is-info"
    ></progress>
  </div>
</template>

<style lang="scss">
.flex-grow-1 {
  flex-grow: 1;
}
</style>
