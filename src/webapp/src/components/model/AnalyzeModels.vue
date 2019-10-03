<script>
import { mapActions, mapGetters, mapState } from 'vuex'

import capitalize from '@/filters/capitalize'
import underscoreToSpace from '@/filters/underscoreToSpace'

export default {
  filters: {
    capitalize,
    underscoreToSpace
  },
  computed: {
    ...mapState('plugins', ['installedPlugins', 'plugins']),
    ...mapGetters('repos', ['hasModels', 'urlForModelDesign']),
    ...mapGetters('plugins', [
      'getIsAddingPlugin',
      'getIsInstallingPlugin',
      'getIsPluginInstalled'
    ]),
    ...mapState('repos', ['models'])
  },
  created() {
    this.$store.dispatch('plugins/getAllPlugins')
    this.$store.dispatch('plugins/getInstalledPlugins')
    this.$store.dispatch('repos/getModels')
  },
  methods: {
    ...mapActions('plugins', ['addPlugin', 'installPlugin']),
    installModel(model) {
      this.addPlugin({ pluginType: 'models', name: model })
        .then(() => this.installPlugin({ pluginType: 'models', name: model }))
        .then(() => this.$store.dispatch('repos/getModels'))
    }
  }
}
</script>

<template>
  <section>
    <div class="columns">
      <div class="column is-one-third">
        <h2 class="title is-5">Custom</h2>
        <div class="content">
          <p>
            <a
              class="has-text-underlined"
              href="https://www.meltano.com/docs/architecture.html#meltano-model"
              target="_blank"
              >Meltano Model</a
            >
            is the glue between your data and click-to-code analysis.
          </p>
          <p>
            Learn more about Meltano Model and how to create
            <a
              class="has-text-underlined"
              href="https://www.meltano.com/docs/tutorial.html#adding-custom-models"
              target="_blank"
              >custom models</a
            >
            so Meltano Analyze can interactively generate SQL queries in
            real-time.
          </p>
        </div>
        <h2 class="title is-5">Available</h2>
        <div class="content">
          <p>
            Below are the models that Meltano ships with in addition to any
            custom models Meltano recognizes in your project.
          </p>
        </div>
        <table
          class="table is-fullwidth is-narrow is-hoverable is-size-7 has-background-transparent"
        >
          <thead>
            <tr>
              <th>Action</th>
              <th>Model</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(modelPlugin, index) in plugins.models">
              <tr :key="`${modelPlugin}-${index}`">
                <td>
                  <div class="buttons">
                    <button
                      v-if="!getIsPluginInstalled('models', modelPlugin)"
                      :class="{
                        'is-loading':
                          getIsAddingPlugin('models', modelPlugin) ||
                          getIsInstallingPlugin('models', modelPlugin)
                      }"
                      class="button is-interactive-primary is-outlined is-block is-small"
                      disabled
                      @click="installModel(modelPlugin)"
                    >
                      Install
                    </button>
                    <a
                      v-else
                      class="button is-small tooltip is-tooltip-warning is-tooltip-right"
                      data-tooltip="Help shape this feature by contributing your ideas"
                      target="_blank"
                      href="https://gitlab.com/meltano/meltano/issues?scope=all&utf8=%E2%9C%93&state=opened&search=uninstall"
                      >Uninstall</a
                    >
                  </div>
                </td>
                <td>
                  <p>{{ modelPlugin }}</p>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
        <progress
          v-if="!plugins.models"
          class="progress is-small is-info"
        ></progress>
      </div>
      <div class="column is-two-thirds">
        <h2 class="title is-5">Installed</h2>
        <template v-if="hasModels">
          <div class="content">
            <p>
              Below are the currently installed models that enable click-to-code
              SQL generation and interactive analysis. Click an Analyze button
              below.
            </p>
          </div>
          <div v-for="(v, model) in models" :key="`${model}-panel`" class="box">
            <div class="content">
              <div class="level level-tight">
                <div class="level-left">
                  <h3 class="is-size-6">
                    {{ v.name | capitalize | underscoreToSpace }}
                  </h3>
                </div>
                <div class="level-right">
                  <h4 class="is-size-7 has-text-grey">
                    {{ v.namespace }}
                  </h4>
                </div>
              </div>
              <hr class="hr-tight" />
              <div
                v-for="design in v['designs']"
                :key="design"
                class="level level-tight"
              >
                <div class="level-left">
                  {{ design | capitalize | underscoreToSpace }}
                </div>
                <div class="level-right">
                  <router-link
                    class="button is-small is-interactive-primary"
                    :to="urlForModelDesign(model, design)"
                    >Analyze</router-link
                  >
                </div>
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="content">
            <p>
              Models are inferred and automatically installed for you based off
              the installed Extractors from your data pipelines. Set up a
              pipeline first.
            </p>
            <router-link
              class="button is-interactive-primary"
              :to="{ name: 'dataSetup' }"
              >Create Data Pipeline</router-link
            >
          </div>
        </template>
      </div>
    </div>
  </section>
</template>

<style lang="scss">
.level-tight:not(:last-child) {
  margin-bottom: 0.5rem;
}
</style>