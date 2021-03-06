import click
from . import cli
from .params import project
from meltano.core.plugin_install_service import PluginInstallService
from meltano.core.plugin_discovery_service import PluginNotFoundError
from meltano.core.project import Project, ProjectNotFound
from meltano.core.project_add_service import ProjectAddService
from meltano.core.tracking import GoogleAnalyticsTracker
from meltano.core.db import project_engine


def install_status_update(data):
    plugin = data["plugin"]

    if data["status"] == "error":
        click.secho(data["message"], fg="red")
        click.secho(data["details"], err=True)
    if data["status"] == "warning":
        click.secho(f"Warning! {data['message']}.", fg="yellow")
    if data["status"] == "success":
        click.secho(f"Installed '{plugin.name}'.", fg="green")


@cli.command()
@project()
def install(project):
    """
    Installs all the dependencies of your project based on the meltano.yml file.
    Read more at https://www.meltano.com/docs/command-line-interface.html#command-line-interface.
    """
    install_service = PluginInstallService(project)
    install_status = install_service.install_all_plugins(install_status_update)
    num_installed = len(install_status["installed"])
    num_failed = len(install_status["errors"])

    fg = "green"
    if num_failed >= 0 and num_installed == 0:
        fg = "red"
    elif num_failed > 0 and num_installed > 0:
        fg = "yellow"

    click.secho(f"{num_installed}/{num_installed+num_failed} plugins installed.", fg=fg)

    tracker = GoogleAnalyticsTracker(project)
    tracker.track_meltano_install()
