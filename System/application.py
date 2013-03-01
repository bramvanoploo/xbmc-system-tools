#http://pythonhosted.org/GitPython/0.3.1/tutorial.html
import config
import git
import log
from inspect import stack

def update():
    try:
        repo = git.Repo(config.root_path)
        remote = git.remote.Remote(repo, 'origin')
        remote.pull()
        log.debug('Successfully updated local repository', stack()[0][3])
        return True
    except:
        log.error('Git pull failed', stack()[0][3])
        return False
    
def is_update_available():
    try:
        repo = git.Repo(config.root_path)
        local_commit = repo.commit()
        remote = git.remote.Remote(repo, 'origin')
        remote_info = remote.fetch()[0]
        remote_commit = remote_info.commit
        return True if not local_commit.hexsha is remote_commit.hexsha else False
    except:
        log.debug('Could not check for new version of software', stack()[0][3])
        return False
    
def get_version():
    repo = git.Repo(config.root_path)
    local_commit = repo.commit()
    return config.version + ' - git ' +local_commit.hexsha