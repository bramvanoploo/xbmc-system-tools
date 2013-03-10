#http://pythonhosted.org/GitPython/0.3.1/tutorial.html
import config
import git
import log
import time
from inspect import stack

def update():
    try:
        repo = git.Repo(config.app_root_path)
        remote = git.remote.Remote(repo, 'origin')
        remote.pull()
        log.debug('Successfully updated local repository', stack()[0][3])
        return True
    except:
        log.error('Git pull failed', stack()[0][3])
        return False

def get_local_commit():
    repo = git.Repo(config.app_root_path)
    return repo.commit()

def get_remote_commit():
    repo = git.Repo(config.app_root_path)
    remote = git.remote.Remote(repo, 'origin')
    remote_info = remote.fetch()[0]
    return remote_info.commit
    
def get_local_version():
    local_commit = get_local_commit()
    return local_commit.hexsha

def get_local_version_time():
    local_commit = get_local_commit()
    return local_commit.committed_date

def get_remote_version():
    remote_commit = get_remote_commit()
    return remote_commit.hexsha

def get_remote_version_time():
    remote_commit = get_remote_commit()
    return remote_commit.committed_date

def get_remote_updates_count():
    local_commit = get_local_commit()
    repo = git.Repo(config.app_root_path)
    remote = git.remote.Remote(repo, 'origin')
    remote_info = remote.fetch()
    count = 0;
    for entry in remote_info:
        if not entry.commit.hexsha.strip() == local_commit.hexsha.strip():
            count += 1
        else:
            break
    return count
    
def is_update_available():
    return False if get_local_version() is get_remote_version() else True
    
def get_version():
    return config.version + ' (' +time.asctime(time.gmtime(get_local_version_time()))+ ')'