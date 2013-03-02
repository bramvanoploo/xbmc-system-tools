#import command
import Database

db = Database.Database('../app.db')

version = "0.5.0"
debug = True

app_root_path = db.get('config', 'app_root_path')
xbmc_user = app_root_path.split('/')[2]
logs_dir = app_root_path+'logs/'

debug_log_file = logs_dir+"debug.log"
error_log_file = logs_dir+"error.log"
info_log_file = logs_dir+"info.log"

home_dir = '/home/'+xbmc_user+'/'
xbmc_home_dir = home_dir+ '.xbmc/'
xbmc_addons_dir = xbmc_home_dir+ 'addons/'
xbmc_userdata_dir = xbmc_home_dir+ 'userdata/'
xbmc_keymaps_dir = xbmc_home_dir+ 'addons/keymaps/'
xbmc_backups_dir = app_root_path+'static/backups/'

xbmc_repositories_url = "http://wiki.xbmc.org/index.php?title=Unofficial_add-on_repositories"
