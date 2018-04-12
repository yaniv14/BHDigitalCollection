import datetime
import os
from contextlib import contextmanager
from io import StringIO

from fabric import operations
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import comment, append
from pathlib import Path

from fabfile_postfix import setup_postfix, setup_opendkim, postfix_log

env.user = "sysop"
env.hosts = ["bh.oglam.hasadna.org.il"]
# Inside each task, env.host will be auto populated from the list above

env.project_name = "bh"
env.clone_url = "https:///github.com/yaniv14/BHDigitalCollection.git"
env.code_dir = f"/home/sysop/{env.project_name}"
env.static_path = f"{env.code_dir}/collected_static/"

env.app_name = "bh"

env.venv_name = env.app_name
env.venvs = f"/home/sysop/.virtualenvs/"
env.venv_path = f"{env.venvs}{env.venv_name}/"
env.venv_command = f"source {env.venv_path}/bin/activate"

# wsgi/uwsgi stuff
env.wsgi_file = "bhdigitalcollection/wsgi.py"
env.stats_port = 9000
env.uwsgi_socket = f"/run/uwsgi/app/{env.app_name}/socket"  # Debian default

env.backup_dir = f"{env.code_dir}/backup/"

APT_PACKAGES = [
    # generic system related packages
    'unattended-upgrades',  # for auto updating your system
    'ntp',  # To keep time synchromized
    'fail2ban',  # to secure against SSH/other attacks

    'mailutils',  # postfix mail server and stuff
    'opendkim',  # SSL for mail
    'opendkim-tools',

    # useful tools
    'git',
    'htop',
    'most',

    'python3',
    'virtualenvwrapper',  # for easily managing virtualenvs

    # required libraries for building some python packages
    'build-essential',
    'python3-dev',
    'libpq-dev',
    'libjpeg-dev',
    'libjpeg8',
    'zlib1g-dev',
    'libfreetype6',
    'libfreetype6-dev',
    'libgmp3-dev',

    # postgres database
    'postgresql',

    # nginx - a fast web server
    'nginx',

    # uwsgi: runs python (django) apps via WSGI
    'uwsgi',
    'uwsgi-plugin-python3',

    'rabbitmq-server',  # for offline tasks via celery (optional)
]


@task
def uptime():
    run("uptime")


@task
def uname():
    run("uname -a")


@task
def apt_upgrade():
    sudo("apt update", pty=False)
    sudo("apt upgrade -y", pty=False)
    sudo("apt autoremove -y", pty=False)


@task
def apt_install():
    # Set some configurations for postfix mail server
    cmd = '''debconf-set-selections <<< "postfix postfix/{} string {}"'''
    sudo(cmd.format('mailname', env.host))
    sudo(cmd.format('main_mailer_type', "'Internet Site'"))

    # install packages
    pkgs = " ".join(APT_PACKAGES)
    sudo(f"DEBIAN_FRONTEND=noninteractive apt-get install -y -q {pkgs}",
         pty=False)


# @task
# def setup_postfix():
#     sudo(f"DEBIAN_FRONTEND=noninteractive dpkg-reconfigure postfix", pty=False)


@task
def apt_install():
    pkgs = " ".join(APT_PACKAGES)
    sudo(f"DEBIAN_FRONTEND=noninteractive apt-get install -y -q {pkgs}",
         pty=False)


@task
def create_postgres_su():
    run("sudo -u postgres createuser -s sysop")
    run("createdb sysop")


@task
def clone_project():
    run(f"git clone {env.clone_url} {env.code_dir}", pty=False)


@task
def create_venv():
    run(f"mkdir -p {env.venvs}")
    run(
        f"virtualenv -p /usr/bin/python3 --prompt='({env.venv_name}) ' {env.venv_path}")


@contextmanager
def virtualenv():
    with cd(env.code_dir):
        with prefix(env.venv_command):
            yield


@task
def upgrade_pip():
    with virtualenv():
        run("pip install --upgrade pip", pty=False)


@task
def pip_install():
    with virtualenv():
        run("pip install -r requirements.txt", pty=False)


@task
def git_pull():
    with virtualenv():
        run("git pull", pty=False)


@task
def deploy():
    git_pull()
    pip_install()


@task
def m(cmd, pty=False):
    with virtualenv():
        run(f"./manage.py {cmd}", pty)


@task
def check():
    m('check')


@task
def send_test_mail():
    m('sendtestemail --admin')


@task
def migrate():
    m('migrate --noinput')


@task
def collect_static():
    m('collectstatic --noinput')


@task
def create_db():
    with virtualenv():
        run("./manage.py sqlcreate -D | psql", pty=False)


UWSGI_CONF = """
[uwsgi]
plugin = python3
virtualenv = {env.venv_path}
chdir = {env.code_dir}
wsgi-file = {env.wsgi_file}
processes = 4
threads = 1
stats = 127.0.0.1:{env.stats_port}
"""


@task
def create_uwsgi_conf():
    conf = UWSGI_CONF.format(env=env)
    filename = f"/etc/uwsgi/apps-available/{env.app_name}.ini"
    enabled = f"/etc/uwsgi/apps-enabled/{env.app_name}.ini"
    put(StringIO(conf), filename, use_sudo=True, )
    sudo(f"ln -sf {filename} {enabled}")
    sudo("service uwsgi stop")
    sudo("service uwsgi start")


NGINX_CONF = """
server {{
    listen 80 default_server;
    return 410;
}}

server {{
    listen 80;
    server_name {host};
    charset     utf-8;

    location /static/ {{
        alias {env.static_path};
    }}

    location / {{
        uwsgi_pass  unix://{env.uwsgi_socket};
        include     uwsgi_params;
    }}
}}"""


@task
def create_nginx_conf():
    conf = NGINX_CONF.format(
        host=env.hosts[0],
        env=env,
    )
    filename = f"/etc/nginx/sites-available/{env.app_name}.conf"
    enabled = f"/etc/nginx/sites-enabled/{env.app_name}.conf"
    put(StringIO(conf), filename, use_sudo=True, )
    sudo(f"ln -sf {filename} {enabled}")

    sudo("rm -vf /etc/nginx/sites-enabled/default")

    sudo("nginx -t")

    sudo("service nginx reload")


@task
def uwsgi_log():
    sudo(f"tail /var/log/uwsgi/app/{env.app_name}.log")


@task
def nginx_log():
    sudo("tail /var/log/nginx/error.log")


@task
def reload_app():
    sudo('systemctl reload uwsgi.service')


@task
def upgrade():
    git_pull()
    pip_install()
    migrate()
    collect_static()
    reload_app()


def make_backup():
    now = datetime.datetime.now()
    filename = now.strftime(
        "{}-%Y-%m-%d-%H-%M.sql.gz".format(env.project_name))
    run('mkdir -p {}'.format(env.backup_dir))
    fullpath = env.backup_dir + '/' + filename
    run('sudo -u postgres pg_dump --no-acl --no-owner {} | gzip > {}'.format(env.app_name,
                                                         fullpath))
    return fullpath


@task
def remote_backup_db():
    path = make_backup()
    operations.get(path)
    run('ls -alh {}'.format(path))


@task
def backup_db():
    files = operations.get(make_backup())
    if len(files) != 1:
        print("no file downloaded!")
        return

    print(f"backup downloaded to: {files[0]}")
    latest = "latest.sql.gz"
    target = Path(files[0])
    local(f"cd {target.parent} && ln -fs {target} {latest}")
    print(f"link created to: {target.parent / latest}")
    return target


@task
def load_local_db_from_file(filename):
    if not os.path.isfile(filename):
        abort("Unknown file {}".format(filename))

    if not confirm(
            "DELETE local db and load from backup file {}?".format(filename)):
        abort("Aborted.")

    drop_command = "drop schema public cascade; create schema public;"
    local('''python3 -c "print('{}')" | python manage.py dbshell'''.format(
        drop_command, filename))

    cmd = "gunzip -c" if filename.endswith('.gz') else "cat"
    local('{} {} | python manage.py dbshell'.format(cmd, filename))


@task
def load_local_db_from_latest():
    filename = backup_db()
    load_local_db_from_file(str(filename))
