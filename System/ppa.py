import log
import command
import software
from inspect import stack

def add(ppa_name):
    if ppa_name.strip().startswith('ppa:') or ppa_name.strip().startswith('deb http://ppa.launchpad.net/') or ppa_name.strip().startswith('deb-src http://ppa.launchpad.net/'):
        success = command.run('sudo add-apt-repository -y "' +ppa_name.strip()+ '"', True)
        software.update_sources()
        return True #Always return True because somehow add-apt-repository command always throws an error, even wen successfull
    else:
        return False

def remove(ppa_name):
    if not ppa_name.strip().startswith('ppa:') or not '/' in ppa_name:
        return False
    success = command.run('sudo add-apt-repository -y -r "' +ppa_name.strip()+ '"', True)
    software.update_sources()
    return success

def purge(ppa_name):
    if not ppa_name.strip().startswith('ppa:') or '/' not in ppa_name:
        return False
    success = command.run('sudo ppa-purge -y '+ppa_name.strip(), True)
    software.update_sources()
    return success

def get_active(key_word):
    ppas_text = command.run('grep -hi "^deb.*launchpad" /etc/apt/sources.list /etc/apt/sources.list.d/*')
    ppas = []
    ppa_lines = ppas_text.split('\n')
    for line in ppa_lines:
        ppa_parts = line.split(' ')
        if len(ppa_parts) == 4:
            ppa_url_parts = ppa_parts[1].split('/')
            ppa_user_name = ppa_url_parts[-3]
            ppa_name = ppa_url_parts[-2]
            ppas.append('ppa:'+ppa_user_name+'/'+ppa_name)
    sorted_ppas = sorted(list(set(ppas)))
    if key_word.strip() == '':
        return sorted_ppas
    else:
        filtered_ppas = []
        for entry in sorted_ppas:
            if key_word in entry:
                filtered_ppas.append(entry)
        return filtered_ppas