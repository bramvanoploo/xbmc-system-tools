#http://pythonhosted.org/GitPython/0.3.1/tutorial.html
import config
import git
import log
from inspect import stack

def update():
    if get_commit_count() > 0:
        try:
            repo = git.Repo(config.root_path)
            origin = repo.remotes.origin
            origin.pull()
            log.debug('Successfully updated local repository (was ' +get_commit_count()+ ' commits behind)', stack()[0][3])
            return True
        except:
            log.error('Git pull failed (' +get_commit_count()+ ' commits behind)', stack()[0][3])
            return False
    else:
        return False
    
def get_commit_count():
    repo = git.Repo(config.root_path)
    local_commit = repo.commit()
    remote = git.remote.Remote(repo, 'origin')
    remote_info = remote.fetch()[0]
    remote_commit = remote_info.commit
    commit_count = 0
    for commit in repo_changes(remote_commit):
        if commit.hexsha == local_commit.hexsha:
            return 0
        commit_count += 1
    return commit_count

def repo_changes(remote_commit):
    next_parent = None
    yield remote_commit
    while len(remote_commit.parents) > 0:
        same_parent(remote_commit.parents)
        for parent in remote_commit.parents:
            yield parent
            next_parent = parent
        remote_commit = next_parent