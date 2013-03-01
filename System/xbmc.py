import config
import command
import os
import time
import urllib2
import helper
import log
import filesystem
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from inspect import stack

def backup_config():
    fileName = str(int(time.time()))+'_xbmc_backup.tar.gz'
    backupPath = config.xbmc_backups_dir+fileName
    if command.run('tar -czf "' +backupPath+ '" -C "' +config.home_directory+ '" ".xbmc"', True):
        return True
    return False

def restore_backup(backup_file):
    filePath = config.xbmc_backups_dir+backup_file
    filesystem.delete_directory(config.xbmc_home_dir)
    if command.run('tar -zxf "' +filePath+ '" -C "' +config.home_directory, True):
        return True
    return False

def get_existing_backup_url_paths():
    files = reversed(sorted(os.listdir(config.xbmc_backups_dir)))
    url_paths = []
    for file in files:
        if os.path.isfile(config.xbmc_backups_dir+file):
            filename_parts = file.split('_')
            timestamp = filename_parts[0]
            try:
                hr_time = datetime.fromtimestamp(int(timestamp))
            except:
                timestamp = 0
                hr_time = file
                pass

            file_size = os.stat(config.xbmc_backups_dir+file).st_size
            entry = {
                'name' : file,
                'timestamp' : timestamp,
                'hr_time' : hr_time,
                'size' : file_size,
                'readable_size' : helper.get_readable_size(file_size)
            }
            url_paths.append(entry)
    return url_paths

def delete_backup(backup_filename):
    return filesystem.delete_file(config.xbmc_backups_dir+backup_filename)

def get_installable_repositories():
    repositories = []
    soup = BeautifulSoup(urllib2.urlopen(config.xbmc_repositories_url).read())
    table = soup.find('table')
    rows = table.findAll('tr')
    for row in rows:
        cols = row.findAll('td')

        if len(cols) is 5:
            repo_website_anchor = cols[0].find('a', href=True)
            if repo_website_anchor:
                repo_name = str(repo_website_anchor.string).replace("\n", "")
                repo_website_url = repo_website_anchor['href']
            else:
                repo_name = str(cols[0].string).replace("\n", "")
                repo_website_url = ''
            repo_description = str(cols[1].string).replace("\n", "")
            repo_owner = str(cols[2].string).replace("\n", "")
            repo_file_anchor = cols[3].find('a', href=True)
            if repo_file_anchor:
                repo_file_url = repo_file_anchor['href']
                repo_file_name = str(repo_file_anchor.string).replace("\n", "")
            else:
                repo_file_url = ''
                repo_file_name = ''
            repo_icon_anchor = cols[4].find('a', href=True)
            if repo_icon_anchor:
                repo_icon_url = repo_icon_anchor['href']
            else:
                repo_icon_url = ''
            entry = {
                'name' : repo_name,
                'website_url' : repo_website_url,
                'description' : repo_description,
                'owner' : repo_owner.replace("\n", ""),
                'download_url' : repo_file_url,
                'file_name' : repo_file_name,
                'icon_url' : repo_icon_url
            }
            repositories.append(entry)
    return repositories

def install_repository(repository_url, repository_filename = 'addon_repo.zip'):
    repo_zip_file_path = '/tmp/'+repository_filename.strip()
    filesystem.delete(repo_zip_file_path)
    try:
        f = urllib2.urlopen(repository_url.strip())
    except:
        log.error('Repository ' +repository_url+ ' could not be downloaded', stack()[0][3])
        return False
    data = f.read()
    with open(repo_zip_file_path, 'wb') as code:
        code.write(data)
    if not os.path.exists(repo_zip_file_path):
        log.error('Repository file' +repo_zip_file_path+ ' does not exist', stack()[0][3])
        return False
    if not command.run('unzip -o ' +repo_zip_file_path+ ' -d ' +config.xbmc_addons_dir):
        log.error('Repository file' +repo_zip_file_path+ ' could not be extracted', stack()[0][3])
        return False
    return command.run('sudo chown -R ' +config.xbmc_user+ ':' +config.xbmc_user+ ' ' +config.xbmc_addons_dir)