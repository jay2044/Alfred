import winreg


def get_installed_programs():
    installed_programs = []
    for key in [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall']:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as registry_key:
            for i in range(0, winreg.QueryInfoKey(registry_key)[0]):
                subkey_name = winreg.EnumKey(registry_key, i)
                with winreg.OpenKey(registry_key, subkey_name) as subkey:
                    try:
                        display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                        install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
                        if display_name and install_location:
                            installed_programs.append((display_name, install_location))
                    except EnvironmentError:
                        pass
    return installed_programs
