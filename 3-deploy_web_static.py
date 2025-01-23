#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers

Usage:
    fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Web server IPs
env.hosts = ['107.23.64.103', '52.6.114.156']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'  # Adjust the path to your SSH key if needed


def do_pack():
    """Generates a .tgz archive from the web_static folder"""
    try:
        # Generate timestamp for unique file naming
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Ensure the versions/ directory exists
        if not isdir("versions"):
            local("mkdir -p versions")

        # Create the archive
        file_name = "versions/web_static_{}.tgz".format(date)
        print("Packing web_static to {}".format(file_name))
        result = local("tar -cvzf {} web_static".format(file_name))

        if result.failed:
            print("Failed to pack web_static")
            return None

        print("web_static packed: {} -> {}Bytes".format(file_name, result))
        return file_name

    except Exception as e:
        print("Error in do_pack: {}".format(e))
        return None


def do_deploy(archive_path):
    """Deploys the archive to the web servers"""
    if not exists(archive_path):
        print("Archive does not exist: {}".format(archive_path))
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        release_path = "/data/web_static/releases/"

        print("Uploading {} to servers...".format(file_n))
        put(archive_path, '/tmp/')

        # Create directory and extract archive
        run('mkdir -p {}{}/'.format(release_path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, release_path, no_ext))

        # Cleanup
        run('rm /tmp/{}'.format(file_n))

        # Move contents and remove old folder
        run('mv {0}{1}/web_static/* {0}{1}/'.format(release_path, no_ext))
        run('rm -rf {}{}/web_static'.format(release_path, no_ext))

        # Remove old symbolic link and create a new one
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(release_path, no_ext))

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print("Error in do_deploy: {}".format(e))
        return False


def deploy():
    """Creates and deploys an archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        print("Failed to create archive.")
        return False

    return do_deploy(archive_path)

