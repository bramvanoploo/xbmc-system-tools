import System
import json
import types
import urllib
import sys
from inspect import stack
from os import path
from flask import Flask, render_template, request, Response, redirect, send_from_directory
from werkzeug import secure_filename

app = Flask(__name__)
#db = System.Database.Database(System.config.installation_database)

System.filesystem.create_directory(System.config.log_directory)
System.filesystem.create_directory(System.config.xbmc_backups_dir)

try:
    server_port = sys.argv[1]
except:
    server_port = "8091"
    pass

def method_exists(method_name):
    try:
        ret = type(eval(method_name))
        return ret in (types.FunctionType, types.BuiltinFunctionType)
    except AttributeError:
        return False

@app.route('/')
def index():
    return redirect('/system_info', 301)

@app.route('/xbmc_backups')
def xbmc_backups():
    return render_template('xbmc_backups.html',
        xbmc_dir_size = System.helper.get_readable_size(System.filesystem.get_directory_size(System.config.xbmc_home_dir)),
        backups = System.xbmc.get_existing_backup_url_paths())
        
@app.route('/xbmc_backups/download/<path:filename>')
def download_backup(filename):
	return send_from_directory(System.config.xbmc_backups_dir, filename)

@app.route('/addon_repositories')
def addon_repositories():
    return render_template('addon_repositories.html',
        repositories = System.xbmc.get_installable_repositories())

@app.route('/system_info')
def system():
    return render_template('system_info.html',
        os                  = System.ubuntu.get_version(),
        kernel              = System.ubuntu.get_kernel_version(),
        gpu_manufacturer    = System.hardware.get_gpu_manufacturer(),
        gpu_type            = System.hardware.get_gpu_type(),
        resolution          = System.hardware.get_current_resolution(),
        max_resolution      = System.hardware.get_maximum_resolution(),
        cpu_type            = System.hardware.get_cpu_type(),
        cpu_core_count      = System.hardware.get_cpu_core_count(),
        cpu_load            = System.hardware.get_cpu_load(),
        total_ram           = System.hardware.get_total_ram(),
        ram_in_use          = System.hardware.get_ram_in_use())

@app.route('/prepare_system')
def prepare_system():
    #db.set('installation_steps', 'prepare_system', 1)
    return render_template('prepare_system.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/system_tools')
def system_tools():
    return render_template('system_tools.html',)

@app.route('/upload_backup',  methods=['POST'])
def upload_backup():
    backup_file = request.files['backup_file']
    backup_file_name = secure_filename(backup_file.filename)
    backup_file.save(path.join(System.config.xbmc_backups_dir, backup_file_name))
    return redirect('/xbmc_backups', 301)

@app.route('/api')
def api():
    result = {
        'success' : False,
        'message' : 'Request not executed'
    }
    if 'method' in request.args and method_exists('System.'+request.args['method']):
        full_request = None
        if 'params' in request.args and request.args['params'] != '':
            full_request = 'System.'+urllib.unquote(request.args['method'])+'(' +urllib.unquote(request.args['params'])+ ')'
        else:
            full_request = 'System.'+urllib.unquote(request.args['method'])+'()'

        System.log.debug('request:' +full_request, stack()[0][3])
        try:
            data = eval(full_request)
            if isinstance(data, bool):
                if not data:
                    result = {
                        'success' : False,
                        'message' : 'An unknown error occurred'
                    }
                else:
                    result = {
                        'success' : True,
                        'result' : True
                    }
            else:
                result = {
                    'success' : True,
                    'result' : data
                }
        except AttributeError as e1:
            System.log.error(str(e1), stack()[0][3])
            result = {
                'success' : False,
                'message' : 'Illegal request: Attribute error (' +str(e1)+ ')'
            }
        except TypeError as e2:
            System.log.error(str(e2), stack()[0][3])
            result = {
                'success' : False,
                'message' : 'Illegal request: Type error (' +str(e2)+ ')'
            }
        except NameError as e3:
            System.log.error(str(e3), stack()[0][3])
            result = {
                'success' : False,
                'message' : 'Illegal Request: Name error (' +str(e3)+ ')'
            }
        except:
            System.log.error('An unknown error occurred', stack()[0][3])
            result = {
                'success' : False,
                'message' : 'An unknown error occurred'
            }
    json_result = json.dumps(result)
    System.log.debug('result:' +json_result, stack()[0][3])
    response = Response(json_result, status=200, mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(server_port), debug=False)
