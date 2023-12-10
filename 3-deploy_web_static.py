#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers using the function deploy.
"""

from fabric.api import local, env
from os.path import exists
from datetime import datetime
from 1-pack_web_static import do_pack
from 2-do_deploy_web_static import do_deploy

env.hosts = ['18.204.13.162', '54.85.22.182']


def deploy():
    """
    Creates and distributes an archive to web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
