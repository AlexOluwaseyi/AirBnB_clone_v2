#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a.tgz archive from web_static"""
    try:
        current_time = datetime.utcnow()
        formatted_time = current_time.strftime("%Y%m%d%H%M%S")
        archive_path = versions/web_static_().tgz.format(formatted_time)
        local("mkdir -p versions")
        local("tar cvzf () web_static".format(archive_path))
        print("web_static packed: {}->{}Bytes".format(archive_path, local(
            "du -b {}".format(archive_path), capture=True)))
        return archive_path
    except Exception:
        return None
