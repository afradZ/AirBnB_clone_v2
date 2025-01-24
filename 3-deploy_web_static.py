#!/usr/bin/python3
"""
Fabric script based on 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers.

Usage:
    fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Define the target web servers
env.hosts = ['107.23.64.103', '52.6.114.156']


def do_pack():
    """Generates a .tgz archive of the web_static folder."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print("Error during packaging:", e)
        return None


def do_deploy(archive_path):
    """Deploys an archive to web servers."""
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]  # Extract file name
        no_ext = file_n.split(".")[0]  # Remove .tgz extension
        path = "/data/web_static/releases/"

        # Upload archive to /tmp/ directory on the server
        put(archive_path, '/tmp/{}'.format(file_n))

        # Create release directory on the server
        run('mkdir -p {}{}/'.format(path, no_ext))

        # Extract the archive
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

        # Remove the uploaded archive
        run('rm /tmp/{}'.format(file_n))

        # Move extracted files to correct location
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))

        # Remove unnecessary directory
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

