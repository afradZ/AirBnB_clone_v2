#!/usr/bin/python3
"""
Fabric script based on 1-pack_web_static.py that distributes an archive
to web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['107.23.64.103', '52.6.114.156']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'  # Update with your SSH key path if needed

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        print("Archive file doesn't exist")
        return False

    try:
        file_name = archive_path.split("/")[-1]  # Extract file name
        no_ext = file_name.split(".")[0]  # Extract name without extension
        release_path = "/data/web_static/releases/{}/".format(no_ext)

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, "/tmp/{}".format(file_name))

        # Create the necessary directories
        run("mkdir -p {}".format(release_path))

        # Uncompress the archive into the release folder
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))

        # Remove the uploaded archive
        run("rm /tmp/{}".format(file_name))

        # Move extracted content to the correct location
        run("mv {0}web_static/* {0}".format(release_path))

        # Remove now empty web_static directory
        run("rm -rf {}web_static".format(release_path))

        # Remove the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print("Deployment failed:", e)
        return False

