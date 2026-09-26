from core.installer import SystemInstaller

def install_gaming_apps(apps_config):
    print("--- Installazione Applicazioni Gaming ---")
    for app in apps_config:
        print(f"Sto installando: {app['name']}...")
        SystemInstaller.install_via_winget(app['winget_id'])

def manage_nvidia_drivers():
    print("--- Controllo Driver Nvidia ---")
    SystemInstaller.install_via_winget("Nvidia.GeForceExperience")