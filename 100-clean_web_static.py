#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives, using the function do_clean.
"""

from fabric.api import env, run, local, runs_once
from datetime import datetime
import os

env.hosts = ['18.204.13.162', '54.85.22.182']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/id_rsa'

#@runs_once
def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    number = int(number)
    if number < 0:
        return
    elif number == 0 or number == 1:
        number = 1

    try:
        # Get the list of archives in the versions folder
        local_archives = os.listdir("versions")
        remote_archives = run(
                'ls -1t /data/web_static/releases').splitlines()

        # Keep only the specified number of archives
        local_archives_to_keep = local_archives[:number]
        remote_archives_to_keep = remote_archives[:number]

        # Delete unnecessary archives in the versions folder
        for archive in local_archives[number:]:
            local('rm -f versions/{}'.format(archive))

        # Delete unnecessary archives on both web servers
        for archive in remote_archives:
            if archive not in remote_archives_to_keep:
                run('rm -rf /data/web_static/releases/{}'.format(archive))

    except Exception as e:
        print(f"Error: {e}")
