class SettingsManager:
    def __init__(self):
        self.settings = {}

    def load_settings(self, settings_file):
        with open(settings_file, "r") as f:
            for line in f:
                if line.startswith("#") or line.startswith("\n"):
                    continue
                else:
                    line = line.split("=")
                    self.settings[line[0]] = line[1].strip()

    def get_setting(self, setting):
        return self.settings[setting]
