#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers using the function deploy.
"""

from fabric.api import local, env
from os.path import exists
from datetime import datetime
from 2-do_deploy_web_static import do_deploy

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)
    except Exception as e:
        return None

def deploy():
    """
    Creates and distributes an archive to web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
