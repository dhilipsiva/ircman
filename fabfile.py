#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: fabfile.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-05-10
"""
__author__ = "dhilipsiva"
__status__ = "development"

"""

"""
import posixpath

from os.path import expanduser, basename, dirname, isfile, join
from datetime import datetime
from pipes import quote
from contextlib import contextmanager

import paramiko
import requests

from fabric.contrib import files
from fabric.state import env
from fabric.decorators import roles, parallel
from fabric.context_managers import cd
from fabric.colors import _wrap_with as wrap_with
from fabric.operations import reboot as _reboot, settings, put
from fabric.api import task, run, local, puts, abort, hide, sudo, prefix, \
    execute
from fabric.contrib.files import exists
from fabric.colors import green

from fabtools import user, require
from fabtools.vagrant import vagrant
from fabtools.python import virtualenv, install_requirements
from fabtools.files import is_file
from fabtools.utils import abspath

paramiko.util.log_to_file('paramiko.log')


# GitHub users who have ssh access. [deploy access]
SSH_USERS = ['dhilipsiva']

green_bg = wrap_with('42')
red_bg = wrap_with('41')

vagrant = vagrant  # Required to silence flake8

env.project = 'ircman'
env.repository = 'git@github.com:dhilipsiva/ircman.git'
env.deploy_user = 'ircman'
env.deploy_user_home = join("/home", env.deploy_user)
env.apps_path = join(env.deploy_user_home, 'apps')
env.code_root = join(env.apps_path, env.project)
env.sockets_path = join(env.code_root, 'node')
env.virtenv = join(env.deploy_user_home, "envs", env.project)
env.nodeenv = join(env.deploy_user_home, "envs", env.project + "_node")
env.deploy_media_path = join(env.code_root, 'uploads')
env.deploy_static_path = env.code_root
env.deploy_media_url = '/uploads/'
env.deploy_media_root = env.deploy_media_path
env.deploy_static_url = '/static/'
env.deploy_static_root = env.deploy_static_path

###
# START gunicorn settings
###
env.gunicorn_bind = "127.0.0.1:8100"
env.gunicorn_logfile = \
    '%(deploy_user_home)s/logs/projects/%(project)s_gunicorn.log' % env
env.rungunicorn_script = \
    '%(deploy_user_home)s/scripts/rungunicorn_%(project)s.sh' % env
env.gunicorn_workers = \
    "$(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 ))"
env.gunicorn_worker_class = "eventlet"
env.gunicorn_loglevel = "debug"
env.gunicorn_pidfile = \
    '%(deploy_user_home)s/%(project)s.pid' % env
###
# END gunicorn settings
###

###
# START sockets settings
###
env.sockets_bind = "127.0.0.1:8008"
env.sockets_logfile = \
    '%(deploy_user_home)s/logs/projects/%(project)s_sockets.log' % env
env.run_sockets_script = \
    '%(deploy_user_home)s/scripts/run_sockets_%(project)s.sh' % env
env.supervisor_sockets = env.project + "_sockets"
env.supervisor_sockets_logfile = \
    '%(deploy_user_home)s/logs/projects/supervisord_%(project)s.log' % env
###
# END sockets settings
###

env.cron_script = \
    "%(deploy_user_home)s/scripts/cron.sh" % env

###
# START gunicorn settings
###
env.supervisor_celery_name = "%(project)s_celery" % env
env.run_celery_script = \
    "%(deploy_user_home)s/scripts/run_celery_%(project)s.sh" % env
env.celery_logfile = \
    "%(deploy_user_home)s/logs/projects/%(project)s_celery.log" % env
###
# END gunicorn settings
###

###
# START nginx settings
###

env.nginx_conf_file = \
    '%(deploy_user_home)s/configs/nginx/%(project)s.conf' % env
# Maximum accepted body size of client request, in MB
env.nginx_client_max_body_size = 300
env.nginx_htdocs = '%(deploy_user_home)s/htdocs' % env
# more info here: http://wiki.nginx.org/HttpSslModule
env.ssl_folder = "%(deploy_user_home)s/%(project)s/ssl" % env
env.ssl_crt = "%(ssl_folder)s/%(project)s.crt" % env
env.ssl_key = "%(ssl_folder)s/%(project)s.key" % env
env.ssl_crt_socket = "%(ssl_folder)s/socket.crt" % env
env.ssl_key_socket = "%(ssl_folder)s/socket.key" % env
env.nginx_avaliable_path = "/etc/nginx/sites-available/"
env.nginx_enable_path = "/etc/nginx/sites-enabled/"
###
# END nginx settings
###
###

###
# START supervisor settings
###
# http://supervisord.org/configuration.html#program-x-section-settings
# default: env.project
env.supervisor_program_name = env.project
env.supervisorctl = '/usr/bin/supervisorctl'  # supervisorctl script
env.supervisor_autostart = 'true'  # true or false
env.supervisor_autorestart = 'true'  # true or false
env.supervisor_redirect_stderr = 'true'  # true or false
env.supervisor_stdout_logfile = \
    '%(deploy_user_home)s/logs/projects/supervisord_%(project)s.log' % env
env.supervisord_conf_file = \
    '%(deploy_user_home)s/configs/supervisord/%(project)s.conf' % env
env.supervisord_celery_conf_file = \
    '%(deploy_user_home)s/configs/supervisord/%(project)s_celery.conf' % env
env.supervisor_dynamic = 'dynamic_scanning'
env.dynamic_path = env.deploy_user_home
env.supervisord_dynamic_conf_file = \
    '%(deploy_user_home)s/%(project)s_dynamic.conf' % env

env.mariadb_cnf_file = "confs/my.cnf"
env.mariadb_cnf_path = "/etc/mysql/conf.d/ircman.cnf"


env.roledefs = {
    'web': [],
    'db': [],
    'task': [],
    'broker': [],
}

env.roledefs['all'] = [h for r in env.roledefs.values() for h in r]
env.roledefs['migrate'] = env.roledefs['web'][:1]
env.roledefs['support'] = env.roledefs['task'][:1]


env.git_allow_dirty = True
env.git_force_push = True

env.nginx_https = False

env.images_directory = "%s/images" % env.deploy_user_home

env.profile_file = "%s/.profile" % env.deploy_user_home


PNGDEFRY_FILE = "master.zip"
PNGDEFRY_ZIP = "https://github.com/xysec/pngdefry/archive/%s" % PNGDEFRY_FILE


@task
def vag():
    """
    A test vagrant config
    """
    host = "127.0.0.1"
    port = 2222
    env.hosts = ["{0}:{1}".format(host, port)]
    env.user = env.deploy_user


@task
def prod():
    """
    Production Instances
    """
    env.nginx_server_name = 'ircman.co'
    env.nginx_socket_name = 'ircman.co'
    env.nginx_https = False
    env.conf_folder = 'prod_confs'
    env.user = env.deploy_user
    env.roledefs = {
        'web': ['52.7.119.55', ],
        'db': ['52.7.119.80', ],
        'task': ['52.7.63.204', ],
        'broker': ['52.7.119.80', ],
    }
    env.roledefs['all'] = [h for r in env.roledefs.values() for h in r]
    env.roledefs['migrate'] = env.roledefs['web'][:1]
    env.roledefs['support'] = env.roledefs['task'][:1]


@task
def new():
    """
    Setup new server
    """
    env.user = env.deploy_user
    env.conf_folder = 'prod_confs'
    env.skip_bad_hosts = True
    env.roledefs = {
        'web': [],
        'db': [],
        'task': [],
        'broker': [],
    }
    env.roledefs['all'] = [h for r in env.roledefs.values() for h in r]
    env.roledefs['migrate'] = env.roledefs['web'][:1]
    env.roledefs['support'] = env.roledefs['task'][:1]
    for key in env.roledefs.keys():
        if not env.roledefs[key]:
            env.roledefs[key] = ['foo.bar', ]


@task
@roles("all")
def ping():
    """
    Just a test task to test connectivity
    """
    run("echo pong")


@task
def add_my_key():
    """
    Add your public key to authorized_keys
    """
    user.add_ssh_public_key(env.deploy_user, expanduser("~/.ssh/id_rsa.pub"))


@task
def create_deploy_user():
    """
    Create the deploy user
    Usage: fab -i path/to/private.pem -H existing_user@host create_deploy_user
    """
    require.users.user(env.deploy_user, shell='/bin/bash')
    require.users.sudoer(env.deploy_user)
    add_my_key()


@task
@roles('all')
def ensure_common_deps():
    require.deb.uptodate_index()
    require.deb.packages([
        "git",
        "libicu-dev",
        "wget",
        "libmysqlclient-dev",
        "libffi-dev",
        "libxslt1-dev",
        "libxml2-dev",
        "python-lxml",
        "libssl-dev",
        "libncurses5-dev",
        "libcairo2-dev",
        "libpango1.0-dev",
        "python-software-properties",
        "python-dev",
        "build-essential",
        "supervisor",
        "vim",
        "python-pip",
        "python-lxml",
        "libgdk-pixbuf2.0-0",
        "shared-mime-info",
        "unzip",
    ])


@task
@roles('web')
def ensure_web_deps():
    """
    Task to ensure dependencies
    """
    require.deb.ppa('ppa:nginx/stable')
    require.deb.uptodate_index()
    require.deb.packages([
        "nginx",
        "vim",
        "nodejs",
        "nodejs-dev",
        "npm",
    ])


@task
@roles('broker')
def ensure_broker_deps():
    """
    Task to ensure dependencies
    """
    require.deb.packages([
        "rabbitmq-server",
        "redis-server",
    ])


def ensure_deps():
    execute(ensure_common_deps)
    execute(ensure_web_deps)
    execute(ensure_broker_deps)


@task
@roles('all')
def ensure_dirs():
    require.files.directories([
        env.virtenv,
        env.apps_path,
        '%(deploy_user_home)s/logs/nginx' % env,
        dirname(env.gunicorn_logfile),
        dirname(env.supervisor_stdout_logfile),
        dirname(env.nginx_conf_file),
        dirname(env.supervisord_conf_file),
        dirname(env.rungunicorn_script),
        env.nginx_htdocs,
        env.ssl_folder,
        env.images_directory,
        ], owner=env.deploy_user)
    run('touch %s' % env.gunicorn_logfile)
    run('touch %s' % env.supervisor_stdout_logfile)
    run('echo "<html><body>nothing here</body></html>"'
        ' > %(nginx_htdocs)s/index.html' % env)


@task
@roles('web', 'task')
def ensure_venv():
    require.python.virtualenv(env.virtenv)


@task
@roles('web', 'task')
def update_venv(with_extras=False):
    """
    Update virtual environment
    """
    with virtualenv(env.virtenv):
        if with_extras:
            install_requirements(
                env.code_root + '/extra-requirements.txt', upgrade=True)
        install_requirements(env.code_root + '/requirements.txt')


def test_nginx_conf():
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('nginx -t -c /etc/nginx/nginx.conf')
    if 'test failed' in res:
        abort(red_bg(
            'NGINX configuration test failed!'
            ' Please review your parameters.'))


@task
@roles('web')
def upload_nginx_conf():
    local_nginx_conf_file_name = 'nginx.conf'
    if env.nginx_https:
        local_nginx_conf_file_name = 'nginx_https.conf'
    local_nginx_conf_file_path = \
        "%s/confs/%s" % (
            dirname(env.real_fabfile), local_nginx_conf_file_name)
    if isfile(local_nginx_conf_file_path):
        ''' we use user defined conf template '''
        template = local_nginx_conf_file_path
    else:
        template = '%s/confs/%s' % (
            env.code_root, local_nginx_conf_file_name)
    files.upload_template(
        template, env.nginx_conf_file, context=env, backup=False,
        use_sudo=True)

    sudo(
        'ln -sf %s %s/%s'
        % (env.nginx_conf_file, env.nginx_enable_path,
           basename(env.nginx_conf_file)))
    sudo('rm -f %s%s' % (env.nginx_enable_path, 'default'))
    test_nginx_conf()
    sudo('nginx -s reload')


@task
@roles('web')
def upload_supervisord_conf():
    local_supervisord_conf_file_path = \
        "%s/confs/supervisord.conf" % dirname(env.real_fabfile)
    if isfile(local_supervisord_conf_file_path):
        '''
        we use user defined supervisord.conf template
        '''
        template = local_supervisord_conf_file_path
    else:
        template = '%s/confs/supervisord.conf' % env.code_root
    files.upload_template(
        template, env.supervisord_conf_file, context=env, backup=False,
        use_sudo=True)
    sudo(
        'ln -sf %s /etc/supervisor/conf.d/%s'
        % (env.supervisord_conf_file, basename(env.supervisord_conf_file)))


@task
@roles('task')
def upload_supervisord_celery_conf():
    local_supervisord_conf_file_path = \
        "%s/confs/supervisord_celery.conf" % dirname(env.real_fabfile)
    if isfile(local_supervisord_conf_file_path):
        ''' we use user defined supervisord.conf template '''
        template = local_supervisord_conf_file_path
    else:
        template = '%s/confs/supervisord_celery.conf' % env.code_root
    files.upload_template(
        template, env.supervisord_celery_conf_file, context=env, backup=False,
        use_sudo=True)
    sudo(
        'ln -sf %s /etc/supervisor/conf.d/%s' % (
            env.supervisord_celery_conf_file,
            basename(env.supervisord_celery_conf_file)))


@task
@roles('web')
def upload_run_sockets_script():
    if isfile('scripts/rungunicorn.sh'):
        '''
        we use user defined rungunicorn file
        '''
        template = 'scripts/run_sockets.sh'
    else:
        template = '%s/scripts/run_sockets.sh' % env.code_root
    files.upload_template(
        template, env.run_sockets_script,
        context=env, backup=False, use_sudo=True)
    sudo('chmod +x %s' % env.run_sockets_script)


@task
@roles('web')
def upload_rungunicorn_script():
    if isfile('scripts/rungunicorn.sh'):
        ''' we use user defined rungunicorn file '''
        template = 'scripts/rungunicorn.sh'
    else:
        template = '%s/scripts/rungunicorn.sh' % env.code_root
    files.upload_template(
        template, env.rungunicorn_script,
        context=env, backup=False, use_sudo=True)
    sudo('chmod +x %s' % env.rungunicorn_script)


@task
@roles('task')
def upload_celery_script():
    if isfile('scripts/runcelery.sh'):
        template = 'scripts/runcelery.sh'
    else:
        template = '%s/scripts/runcelery.sh' % env.code_root
    files.upload_template(
        template, env.run_celery_script,
        context=env, backup=False, use_sudo=True)
    sudo('chmod +x %s' % env.run_celery_script)


@roles('web', 'task')
def reload_supervisorctl():
    sudo('%(supervisorctl)s reread' % env)
    sudo('%(supervisorctl)s reload' % env)


@task
@roles('web', 'task')
def supervisor_restart():
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('%(supervisorctl)s restart all' % env)
    if 'ERROR' in res:
        print red_bg("%s NOT STARTED!" % env.supervisor_program_name)


def gunicorn_hup():
    """
    send restart signal to gunicorn
    """
    sudo("kill -HUP `cat %s`" % env.gunicorn_pidfile)


@task
def sync_auth_keys():
    """
    Add multiple public keys to the user's authorized SSH keys from GitHub.
    """

    ssh_dir = posixpath.join(user.home_directory(env.user), '.ssh')
    require.files.directory(ssh_dir, mode='700', owner=env.user, use_sudo=True)
    authorized_keys_filename = posixpath.join(ssh_dir, 'authorized_keys')
    require.files.file(
        authorized_keys_filename, mode='600', owner=env.user, use_sudo=True)

    sudo('cat /dev/null > %s' % quote(authorized_keys_filename))

    for gh_user in SSH_USERS:
        r = requests.get("https://api.github.com/users/%s/keys" % gh_user)
        for key in r.json():
            sudo(
                "echo %s >> %s"
                % (quote(key["key"]), quote(authorized_keys_filename)))


@task
@roles('migrate')
def migrate():
    """
    Migrate the database
    """
    with virtualenv(env.virtenv):
        with cd(env.code_root):
            run("./manage.py migrate")


@task
@roles('web')
def collect_static():
    """
    Collect the static files
    """
    with virtualenv(env.virtenv):
        run("cd %s && python manage.py collectstatic --noinput" %
            env.code_root)


@task
@roles('all')
def reboot():
    _reboot()


def create_nodeenv(directory):
    directory = quote(directory)
    command = 'nodeenv %s' % directory
    run(command)


def nodeenv_exists(directory):
    """
    Check if a Python `virtual environment`_ exists.
    .. _virtual environment: http://www.virtualenv.org/
    """
    return is_file(posixpath.join(directory, 'bin', 'node'))


@task
@roles('web')
def ensure_nodeenv(
        system_site_packages=False, venv_python=None,
        use_sudo=False, user=None, clear=False, prompt=None,
        virtualenv_cmd='nodeenv', pip_cmd='npm', python_cmd='node'):
    sudo("pip install nodeenv")
    """
    Require a Python `virtual environment`_.
    ::
        from fabtools import require
        require.python.virtualenv('/path/to/venv')
    .. _virtual environment: http://www.virtualenv.org/
    """

    if not nodeenv_exists(env.nodeenv):
        create_nodeenv(env.nodeenv)


@contextmanager
def nodeenv(directory, local=False):
    """
    Context manager to activate an existing Python `virtual environment`_.
    ::
        from fabric.api import run
        from fabtools.python import nodeenv
        with nodeenv('/path/to/nodeenv'):
            run('python -V')
    .. _virtual environment: http://www.nodeenv.org/
    """

    # Build absolute path to the nodeenv activation script
    nodeenv_path = abspath(directory, local)
    activate_path = join(nodeenv_path, 'bin', 'activate')

    # Source the activation script
    with prefix('. %s' % quote(activate_path)):
        yield


@task
@roles('web')
def ensure_npm_deps():
    """docstring for ensure_npm_deps"""
    with nodeenv(env.nodeenv):
        run("cd %s && npm install" % env.sockets_path)


def append_to_profile(text):
    """
    docstring for append_to_profile
    """
    files.append(env.profile_file, text)


@task
@roles('broker')
def update_redis_conf():
    files.comment("/etc/redis/redis.conf", "bind 127.0.0.1", use_sudo=True)
    files.append("/etc/redis/redis.conf", "bind 0.0.0.0", use_sudo=True)


@task
@roles('all')
def allow_dirty():
    """
    allow pushing even when the working copy is dirty
    """
    env.git_allow_dirty = True


@task
def force_push():
    """
    allow pushing even when history will be lost
    """
    env.git_force_push = True


def git_init():
    """
    create a git repository if necessary [remote]
    """

    # check if it is a git repository yet
    if exists('%s/.git' % env.code_root):
        return

    puts(green('Creating new git repository ') + env.code_root)

    # create repository folder if necessary
    run('mkdir -p %s' % env.code_root, quiet=True)

    with cd(env.code_root):
        # initialize the remote repository
        run('git init')

        # silence git complaints about pushes coming in on the current branch
        # the pushes only seed the immutable object store and do not modify the
        # working copy
        run('git config receive.denyCurrentBranch ignore')


@task
@roles('web', 'task')
def git_seed(commit=None, ignore_untracked_files=False):
    """
    seed a git repository (and create if necessary) [remote]
    """

    # check if the local repository is dirty
    dirty_working_copy = git_is_dirty(ignore_untracked_files)
    if dirty_working_copy:
        abort(
            'Working copy is dirty. This check can be overridden by\n'
            ' try adding allow_dirty to your call.')

    # check if the remote repository exists and create it if necessary
    git_init()

    # use specified commit or HEAD
    commit = commit or git_head_rev()

    # finish execution if remote repository has commit already
    if git_exists(env.code_root, commit):
        puts(green('Commit ') + commit + green(' exists already'))
        return

    # push the commit to the remote repository
    #
    # (note that pushing to the master branch will not change the contents
    # of the working directory)

    puts(green('Pushing commit ') + commit)

    with settings(warn_only=True):
        force = (env.git_force_push) and '-f' or ''
        push = local(
            'git push git+ssh://%s@%s:%s%s %s:refs/heads/master %s' % (
                env.user, env.host, env.port, env.code_root,
                commit, force))

    if push.failed:
        abort(
            '%s is a non-fast-forward\n'
            'push. The seed will abort so you don\'t lose information.'
            ' If you are doing this\nintentionally try user'
            ' force_push and add it to your call.' % commit)


def git_exists(repo_path, commit):
    """
    check if the specified commit exists in the repository [remote]
    """

    with cd(repo_path):
        if run('git rev-list --max-count=1 %s' % commit,
                warn_only=True, quiet=True).succeeded:
            return True


@task
@roles('web', 'task')
def git_reset(commit=None):
    """
    reset the working directory to a specific commit [remote]
    """

    # use specified commit or HEAD
    commit = commit or git_head_rev()

    puts(green('Resetting to commit ') + commit)

    # reset the repository and working directory
    with cd(env.code_root):
        run('git reset --hard %s' % commit)


def git_head_rev():
    """
    find the commit that is currently checked out [local]
    """
    return local('git rev-parse HEAD', capture=True)


def git_is_dirty(ignore_untracked_files):
    """
    check if there are modifications in the repository [local]
    """

    if env.git_allow_dirty:
        return False

    untracked_files = '--untracked-files=no' if ignore_untracked_files else ''
    return local('git status %s --porcelain' % untracked_files,
                 capture=True) != ''


@task
@roles('web', 'task')
def upload_key_files():
    [put('%s/%s' % (env.conf_folder, f), env.code_root) for f in [
        "local_settings.py",
    ]]


@task
@roles('web')
def upload_index_file():
    suffix = ''
    if env.conf_folder == 'staging_confs':
        suffix = '_staging'
    put('generated/index%s.html' % suffix,
        '%s/generated/index.html' % env.code_root)

mysql_cmd = "mysql -u root -e '%s'"


@task
@roles('db')
def fix_collation():
    """
    Fix `Illegal mix of collations (latin1_swedish_ci,IMPLICIT)
    and (utf8_general_ci,COERCIBLE)` Error
    http://stackoverflow.com/a/1008336/1235072
    """
    fix_sql = 'SET collation_connection = "utf8_general_ci"; \
        USE %s ; \
        ALTER DATABASE %s CHARACTER SET utf8 COLLATE utf8_general_ci; \
        ALTER TABLE %s CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;'\
        % (env.project, env.project, 'webfrontend_contact')
    run(mysql_cmd % fix_sql)


@task
@roles('db')
def setup_db():
    require.deb.uptodate_index()
    require.deb.package("software-properties-common")
    sudo(
        "apt-key adv --recv-keys"
        " --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db")
    sudo(
        "sudo add-apt-repository"
        " 'deb http://mariadb.bytenet.in//repo/10.0/ubuntu trusty main'")
    require.deb.uptodate_index()
    require.deb.package("mariadb-server")
    run("mysql_secure_installation")
    put(env.mariadb_cnf_file, env.mariadb_cnf_path, use_sudo=True)
    sudo("service mysql restart")
    password = raw_input("Please Enter password: ")
    create_sql = "CREATE DATABASE %s;" % env.project
    sql = 'CREATE USER "' + env.deploy_user + '"@"%" ' \
        + ' IDENTIFIED BY "' + password + '";' \
        + ' GRANT ALL PRIVILEGES ON *.* TO "' + env.deploy_user + '"@"%";' \
        + ' FLUSH PRIVILEGES;'
    run(mysql_cmd % create_sql)
    run(mysql_cmd % sql)
    files.comment(env.mariadb_cnf_path, "skip-grant-tables", use_sudo=True)
    sudo("service mysql restart")


@task
def setup():
    """
    Setup a new machine
    """
    puts(green_bg('Start setup...'))
    start_time = datetime.now()
    # ensure_deps()
    # execute(ensure_dirs)
    # execute(update_redis_conf)
    # execute(git_seed)
    # execute(git_reset)
    # execute(ensure_venv)
    # execute(ensure_nodeenv)
    # execute(ensure_npm_deps)
    # execute(update_venv, True)
    # execute(upload_key_files)
    # execute(upload_index_file)
    # execute(migrate)
    execute(collect_static)
    execute(upload_rungunicorn_script)
    execute(upload_celery_script)
    execute(upload_run_sockets_script)
    execute(upload_supervisord_conf)
    execute(upload_supervisord_celery_conf)
    execute(upload_nginx_conf)
    execute(reboot)
    end_time = datetime.now()
    finish_message = \
        '[%s] Correctly finished in %i seconds' % (
            green_bg(end_time.strftime('%H:%M:%S')),
            (end_time - start_time).seconds)
    puts(finish_message)


@task
def deploy():
    """
    Task to do a deploy
    """
    puts(green_bg('Start deploy...'))
    start_time = datetime.now()
    execute(git_seed)
    execute(git_reset)
    execute(update_venv)
    execute(upload_key_files)
    execute(upload_index_file)
    execute(ensure_npm_deps)
    execute(migrate)
    execute(collect_static)
    execute(upload_rungunicorn_script)
    execute(upload_celery_script)
    execute(upload_run_sockets_script)
    execute(upload_supervisord_conf)
    execute(upload_supervisord_celery_conf)
    execute(reload_supervisorctl)
    execute(supervisor_restart)
    execute(upload_nginx_conf)
    end_time = datetime.now()
    finish_message = \
        '[%s] Correctly deployed in %i seconds' % (
            green_bg(end_time.strftime('%H:%M:%S')),
            (end_time - start_time).seconds)
    puts(finish_message)


@roles("task")
@task
def get_file_stuff(file_id):
    """
    get_file_stuff
    """
    with virtualenv(env.virtenv):
        with cd(env.code_root):
            run("./manage.py get_file_stuff %s" % file_id)


@task
@parallel
def qd():
    """
    Quick Deploy
    """
    prod()
    execute(git_seed)
    execute(git_reset)
    execute(migrate)
    execute(supervisor_restart)
