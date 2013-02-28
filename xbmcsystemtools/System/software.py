import apt
import apt_pkg
import command
import log
from inspect import stack

def update_sources():
    try:
        apt_cache = apt.cache.Cache()
        apt_cache.update()
        success = apt_cache.commit(apt.progress.TextFetchProgress(), apt.progress.InstallProgress())
        #apt_cache.close()
        return success
    except AttributeError as e:
        log.error('AttributeError: ' +str(e), stack()[0][3])
        #apt_cache.close()
        return False

def dist_upgrade():
    apt_cache = apt.cache.Cache()
    apt_cache.update()
    apt_cache.open(None)
    apt_cache.upgrade(True)
    success = apt_cache.commit(apt.progress.TextFetchProgress(), apt.progress.InstallProgress())
    #apt_cache.close()
    return success

def install(package_name):
    apt_pkg.init()
    apt_pkg.PkgSystemLock()
    apt_cache = apt.cache.Cache()
    pkg = apt_cache[package_name.strip()]
    if package_name.strip() in apt_cache:
        if pkg.isInstalled:
            apt_pkg.PkgSystemUnLock()
            log.info('Trying to install a package that is already installed (' +package_name.strip()+ ')', stack()[0][3])
            #apt_cache.close()
            return False
        else:
            pkg.mark_install()
            try:
                apt_pkg.PkgSystemUnLock()
                result = apt_cache.commit()
                #apt_cache.close()
                return result
            except SystemError as e:
                log.error('SystemError: ' +str(e), stack()[0][3])
                #apt_cache.close()
                return False
    else:
        #apt_cache.close()
        log.error('Unknown package selected (' +package_name.strip()+ ')', stack()[0][3])
        return False

def remove(package_name, purge = False):
    apt_pkg.init()
    apt_pkg.PkgSystemLock()
    apt_cache = apt.cache.Cache()
    pkg = apt_cache[package_name.strip()]
    if package_name.strip() in apt_cache:
        if not pkg.isInstalled:
            apt_pkg.PkgSystemUnLock()
            log.info('Trying to uninstall a package that is not installed (' +package_name.strip()+ ')', stack()[0][3])
            return False
        else:
            pkg.mark_delete(purge)
            try:
                apt_pkg.PkgSystemUnLock()
                result = apt_cache.commit()
                #apt_cache.close()
                return result
            except SystemError as e:
                log.error('SystemError: ' +str(e), stack()[0][3])
                #apt_cache.close()
                return False
    else:
        #apt_cache.close()
        log.info('Unknown package selected (' +package_name.strip()+ ')', stack()[0][3])
        return False

def auto_clean():
    return command.run('sudo apt-get -y autoclean', True)

def auto_remove():
    return command.run('sudo apt-get -y autoremove', True)

def search(package_name, installed_packes):
    apt_cache = apt.cache.Cache()
    apt_cache.open(None)
    packages = apt_cache.keys()
    if installed_packes:
        result = [value for value in packages if apt_cache[value].isInstalled and package_name.strip() in value]
    else:
        result = [value for value in packages if not apt_cache[value].isInstalled and package_name.strip() in value]
    #apt_cache.close()
    return sorted(result)

def is_package_installed(package_name):
    apt_cache = apt.cache.Cache()
    apt_cache.open()
    if package_name.strip() in cache and cache[package_name.strip()].is_installed:
        apt_cache.close()
        return True
    #apt_cache.close()
    return False

def package_exists(package_name):
    apt_cache = apt.cache.Cache()
    apt_cache.open()
    if package_name.strip() in cache:
        apt_cache.close()
        return True
    #apt_cache.close()
    return False