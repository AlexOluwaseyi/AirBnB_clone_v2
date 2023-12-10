#!/usr/bin/python3
"""
 a Fabric script that generates a .tgz archive from the contents
 of the web_static folder of your AirBnB Clone repo
 """

from fabric.api import local
from datetime import datetime
import os


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
