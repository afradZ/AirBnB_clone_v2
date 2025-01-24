#!/usr/bin/python3
"""
Deletes out-of-date archives
Usage:
    fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu
"""

import os
from fabric.api import env, lcd, local, run, cd

env.hosts = ['107.23.64.103', '52.6.114.156']

def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = max(int(number), 1)

    # Clean local archives
    archives = sorted(os.listdir("versions"))
    archives_to_delete = archives[:-number]
    with lcd("versions"):
        for archive in archives_to_delete:
            local("rm ./{}".format(archive))

    # Clean remote archives
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        archives_to_delete = archives[:-number]
        for archive in archives_to_delete:
            run("rm -rf ./{}".format(archive))

