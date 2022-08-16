# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

from octoprint_alveocontrol.alveo import AlveoController


class AlveocontrolPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.EventHandlerPlugin,
):
    def on_after_startup(self):
        self.alveo = AlveoController(self._settings.get(["serial_port"]))

    # ~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {"serial_port": "/dev/ttyAMA0", "speed": 50}

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.alveo = AlveoController(self._settings.get(["serial_port"]))
        self.alveo.speed(int(self._settings.get(["speed"])))

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def on_event(self, event, payload):
        if event == "PrintStarted":
            self.alveo.start(int(self._settings.get(["speed"])))
        elif event in ["PrintDone", "PrintFailed", "PrintCancelled"]:
            self.alveo.stop()
            self.alveo.fast()

    # ~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "alveocontrol": {
                "displayName": "Alveocontrol Plugin",
                "displayVersion": self._plugin_version,
                # version check: github repository
                "type": "github_release",
                "user": "AnotherStranger",
                "repo": "OctoPrint-Alveocontrol",
                "current": self._plugin_version,
                # update method: pip
                "pip": "https://github.com/AnotherStranger/OctoPrint-Alveocontrol/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Alveocontrol Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = AlveocontrolPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
