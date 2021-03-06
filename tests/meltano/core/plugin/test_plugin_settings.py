import pytest

from meltano.core.plugin import PluginRef
from meltano.core.plugin.setting import PluginSetting
from meltano.core.plugin.settings_service import (
    PluginSettingValueSource,
    REDACTED_VALUE,
)


def test_create(session):
    setting = PluginSetting(
        name="api_key.test.test", namespace="gitlab", value="C4F3C4F3", enabled=True
    )

    session.add(setting)
    session.commit()

    fetched = session.query(PluginSetting).first()
    assert setting == fetched


@pytest.fixture(scope="class")
def env_var(plugin_discovery_service, plugin_settings_service):
    def _wrapper(plugin: PluginRef, setting_name):
        plugin_def = plugin_discovery_service.find_plugin(plugin.type, plugin.name)

        return plugin_settings_service.setting_env({"name": setting_name}, plugin_def)

    return _wrapper


@pytest.fixture
def subject(session, project_add_service, tap, plugin_settings_service):
    plugin = project_add_service.add("extractors", tap.name)

    return plugin_settings_service


class TestPluginSettingsService:
    def test_get_value(self, session, subject, project, tap, env_var, monkeypatch):
        # returns the default value when unset
        assert subject.get_value(session, tap, "test") == (
            "mock",
            PluginSettingValueSource.DEFAULT,
        )

        # overriden by an PluginSetting db value when set
        setting = subject.set(session, tap, "test", "THIS_IS_FROM_DB")
        assert subject.get_value(session, tap, "test") == (
            "THIS_IS_FROM_DB",
            PluginSettingValueSource.DB,
        )

        # but only if enabled
        setting.enabled = False
        session.merge(setting)
        session.commit()
        assert subject.get_value(session, tap, "test") == (
            "mock",
            PluginSettingValueSource.DEFAULT,
        )

        # overriden via the `meltano.yml` configuration
        original_meltano = project.meltano
        with project.meltano_update() as meltano:
            meltano["plugins"]["extractors"][0]["config"] = {"test": 42}

        assert subject.get_value(session, tap, "test") == (
            42,
            PluginSettingValueSource.MELTANO_YML,
        )

        # revert back to the original
        with project.meltano_update() as meltano:
            meltano.update(original_meltano)

        # overriden via ENV
        monkeypatch.setenv(env_var(tap, "test"), "N33DC0F33")
        assert subject.get_value(session, tap, "test") == (
            "N33DC0F33",
            PluginSettingValueSource.ENV,
        )

    def test_as_config(self, subject, session, tap):
        EXPECTED = {"test": "mock", "start_date": None, "secure": None}
        full_config = subject.as_config(session, tap)
        redacted_config = subject.as_config(session, tap, redacted=True)

        for k, v in EXPECTED.items():
            assert full_config.get(k) == v
            assert redacted_config.get(k) == v

    def test_as_config_redacted(self, subject, session, tap):
        # ensure values are redacted when they are set
        subject.set(session, tap, "secure", "thisisatest")
        config = subject.as_config(session, tap, redacted=True)

        assert config["secure"] == REDACTED_VALUE

        # although setting the REDACTED_VALUE does nothing
        subject.set(session, tap, "secure", REDACTED_VALUE)
        config = subject.as_config(session, tap)
        assert config["secure"] == "thisisatest"

    def test_as_env(self, subject, session, tap, env_var):
        config = subject.as_env(session, tap)

        assert config.get(env_var(tap, "test")) == "mock"
        assert config.get(env_var(tap, "start_date")) == "None"
        assert config.get(env_var(tap, "secure")) == "None"

    def test_unset(self, session, subject, tap):
        # overriden by an PluginSetting db value when set
        setting = subject.set(session, tap, "test", "THIS_IS_FROM_DB")
        assert session.query(PluginSetting).count() == 1

        subject.unset(session, tap, "test")
        assert session.query(PluginSetting).count() == 0


class TestCustomPluginSettingsService:
    @pytest.fixture(scope="class", autouse=True)
    def custom_setting(subject, project, config_service, tap):
        with project.meltano_update() as meltano:
            custom_settings = [
                {
                    "name": "custom_setting",
                    "value": "pytest",
                    "kind": "pytest",
                    "env": "PYTEST_CUSTOM_SETTING",
                },
                {"name": "test", "value": "override"},
            ]

            tap_mock = meltano["plugins"]["extractors"][0]
            tap_mock["settings"] = custom_settings

    def test_setting_exists(self, subject, tap):
        exists = lambda setting: setting["name"] == "custom_setting"

        assert any(map(exists, subject.definitions(tap)))

    def test_precedence(self, subject, session, tap):
        value, _ = subject.get_value(session, tap, "test")

        assert value == "override"
