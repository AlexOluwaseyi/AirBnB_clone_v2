#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web
servers using the function deploy.
"""

from os.path import exists
from datetime import datetime
from fabric.api import env, put, run, sudo, local, runs_once
from os import path
import os


env.hosts = ['18.204.13.162', '54.85.22.182']
env.user = 'ubuntu'
env.key = '/root/.ssh/id_rsa'


@runs_once
def do_pack():
    """Generate a .tgz archive from the contents of web_static."""
    try:
        # Create the 'versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Create the archive filename
        now = datetime.utcnow()
        archive_name = "web_static_{}{:02}{:02}{:02}{:02}{:02}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )

        # Archive the web_static folder
        print('Packing web_static to versions/{}.tgz'.format(archive_name))
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the archive path
        archive_path = os.path.join("versions", archive_name)

        # Get the size of the created archive
        archive_size = os.path.getsize("versions/{}".format(archive_name))

        print("web_static packed: versions/{} -> {}Bytes".format(
            archive_name, archive_size
            ))
        return archive_path

    except Exception as e:
        print(f"Error: {e}")
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""

    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive_filename>
        archive_filename = archive_path.split('/')[-1]
        release_folder = '/data/web_static/releases/{}'.format(
            archive_filename.split('.')[0]
            )
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(
            archive_filename, release_folder)
            )

        # Delete the uploaded archive
        run('sudo rm /tmp/{}'.format(archive_filename))

        # Move files in ./web_static subfolder to parent folder
        run('cp -r {}/web_static/* {}/'.format(
            release_folder, release_folder)
            )
        run('sudo rm -r {}/web_static'.format(release_folder))

        # Create a new symbolic link to the new version of the code
        run('sudo rm -rf /data/web_static/current')
        current_link = '/data/web_static/current'
        run('sudo ln -sf {} {}'.format(release_folder, current_link))

        run('sudo chown -R ubuntu:ubuntu /data/')

        print('New version deployed!')
        return True

    except Exception as e:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        print("no archive")
        return False

    return do_deploy(archive_path)

'''
if __name__ == '__main__':
    """
    Call theh deploy function"
    """
    deploy()
'''
