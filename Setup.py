import os
import subprocess
import json
import config

def install_packages():
    packages = ["telebot", "requests", "schedule"]
    for package in packages:
        subprocess.check_call([os.sys.executable, "-m", "pip", "install", package])

def update_devcontainer():
    devcontainer_path = ".devcontainer/devcontainer.json"
    devcontainer_content = {
        "name": "My Codespace",
        "image": "mcr.microsoft.com/vscode/devcontainers/python:3.8",
          "postStartCommand": "${config:POST_START_COMMAND}"
        "customizations": {
            "vscode": {
                "settings": {
                    "python.pythonPath": "/usr/local/bin/python",
                    "terminal.integrated.shell.linux": "/bin/bash"
                },
                "extensions": [
                    "ms-python.python"
                ]
            }
        }
    }

    os.makedirs(os.path.dirname(devcontainer_path), exist_ok=True)
    with open(devcontainer_path, 'w') as file:
        json.dump(devcontainer_content, file, indent=4)

def update_vscode_settings():
    settings_path = os.path.expanduser("~/.config/Code/User/settings.json")
    # Alternative path for Windows
    if not os.path.exists(settings_path):
        settings_path = os.path.expanduser("~/AppData/Roaming/Code/User/settings.json")

    settings_to_add = {
        "workbench.colorTheme": "Default High Contrast",
        "security.workspace.trust.untrustedFiles": "open",
        "terminal.integrated.defaultProfile.windows": "Git Bash",
        "terminal.integrated.inactiveTimeout": 0,
        "editor.fontSize": 14,
        "files.autoSave": "onFocusChange"
    }

    if os.path.exists(settings_path):
        with open(settings_path, 'r+') as file:
            try:
                current_settings = json.load(file)
            except json.JSONDecodeError:
                current_settings = {}

            current_settings.update(settings_to_add)

            file.seek(0)
            json.dump(current_settings, file, indent=4)
            file.truncate()
    else:
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        with open(settings_path, 'w') as file:
            json.dump(settings_to_add, file, indent=4)

def configure_firewall():
    # Install ufw if not already installed
    subprocess.check_call(["sudo", "apt", "update"])
    subprocess.check_call(["sudo", "apt", "install", "-y", "ufw"])

    # Enable ufw and allow ports 10000-30000/udp
    subprocess.check_call(["sudo", "ufw", "enable"])
    subprocess.check_call(["sudo", "ufw", "allow", "10000:30000/udp"])

    # Check ufw status
    subprocess.check_call(["sudo", "ufw", "status"])

    # Display iptables rules
    subprocess.check_call(["sudo", "iptables", "-L"])

def run_git_commands():
    commands = [
        "git add .devcontainer/devcontainer.json",
        "git commit -m 'Add devcontainer.json for Codespaces'",
        "git push origin main"
    ]
    for command in commands:
        subprocess.check_call(command, shell=True)

if __name__ == "__main__":
    install_packages()
    update_devcontainer()
    update_vscode_settings()
    configure_firewall()
    run_git_commands()