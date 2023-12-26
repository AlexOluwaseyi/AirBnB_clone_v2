#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the
function do_deploy.
"""


from fabric.api import env, put, run, sudo, local
from datetime import datetime
import os


env.hosts = ['18.204.13.162', '54.85.22.182']
env.user = 'ubuntu'

'''
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

    print('New version deployed!')
    return True
'''
def do_pack():
    '''
    A function that generaees a .tgx archive from the web_static folder
    '''
    if not os.path.exists('versions'):
        os.makedirs('versions')

    filename = time.strftime("%Y%m%d%H%M%S")
    fullpath = "versions/web_static_{}.tgz".format(filename)
    try:
        local("tar -cvzf {} web_static".format(fullpath))
        return fullpath
    except:
        return None


def do_deploy(archive_path):
    '''
    Distributes an archive to my webservers
    '''
    if not os.path.isfile(archive_path):
        return False

    # Upload the archive to the server
    put(archive_path, '/tmp/')

    # Create directory where we will extract the file to
    file_name = archive_path.split('/')[-1]  # Get file name
    dir_path = '/data/web_static/releases/{}'.format(file_name.split('.')[0])
    run('mkdir -p {}'.format(dir_path))

    # Uncompress the archive to the folder
    server_archive_path = '/tmp/' + file_name  # Path of archive in server
    run('tar -xzf {} -C {}'.format(server_archive_path, dir_path))

    # Delete the archive from the web server
    run('rm -rf {}'.format(server_archive_path))

    # Delete the symbolic link
    run('rm -rf /data/web_static/current')

    # Move the files from web_static to web_static_<number>
    run('mv {}/web_static/* {}'.format(dir_path, dir_path))
    run('rm -rf {}/web_static'.format(dir_path))

    # Create a new symbolic link
    run('ln -s {} /data/web_static/current'.format(dir_path))

    return True
