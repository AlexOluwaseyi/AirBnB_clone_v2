#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the
function do_deploy.
"""

from fabric.api import env, put, run, sudo
from os import path

env.hosts = ['18.204.13.162', '54.85.22.182']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not path.exists(archive_path):
        print("archive does not exist")
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
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Delete the uploaded archive
        run('rm /tmp/{}'.format(archive_filename))

        # Move files in ./web_static subfolder to parent folder
        run('mv {}/web_static/* {}/'.format(release_folder, release_folder))

        # Create a new symbolic link to the new version of the code
        current_link = '/data/web_static/current'
        run('ln -sf {} {}'.format(release_folder, current_link))

        print('New version deployed!')
        return True

    except Exception as e:
        return False


if __name__ == "__main__":
   do_deploy(archive_path)
