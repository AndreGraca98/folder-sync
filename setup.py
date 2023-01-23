import json
from pathlib import Path
from subprocess import check_call

from setuptools import setup
from setuptools.command.install import install

script = f"""
cp main.py sync-folders
chmod +x sync-folders
mkdir -p {Path.home()}/bin
cp -r folder_sync {Path.home()}/bin
cp sync-folders {Path.home()}/bin
"""


class PostInstallCommand(install):
    """Pre-installation for installation mode."""

    def run(self):
        install.run(self)
        for cmd in script.split("\n"):
            if cmd:
                print("cmd:", cmd)
                check_call(cmd.split())


setup(
    name="folder-sync",
    version=json.load(open("folder_sync/version.json"))["version"],
    description="Synchronize two folders: source and replica. Keep a full, identical copy of source folder at replica folder.",
    author="André Graça",
    author_email="andrepgraca@gmail.com",
    platforms="Python",
    packages=["folder_sync"],
    install_requires=["python-crontab"],
    cmdclass={
        "install": PostInstallCommand,
    },
)
