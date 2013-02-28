function Api() {
	this.request = function(pstrMethod, pstrParams, pfCallback) {
		var lstrParams = (pstrParams == undefined)? '' : pstrParams;
		var lfCallback = (pfCallback == undefined)? function(){} : pfCallback;

		$.ajax({
			type: 'GET',
			url: '/api',
			dataType: 'json',
			cache: false,
			data: {
				method: pstrMethod,
				params: lstrParams
			},
			success: function(data, textStatus, jqXHR) {
				lfCallback(data);
			},
			error: function(jqXHR, textStatus, errorThrown) {

			}
		});
	}

	this.getOperatingSystem = function(pstrTarget) {
		this.request('ubuntu.get_version', '', function(poData){
			if(poData && poData.success) {
				$(pstrTarget).html(poData.result);
			}
		});
	}

	this.getCpuLoad = function(pstrTarget) {
		this.request('hardware.get_cpu_load', '', function(poData){
			if(poData && poData.success) {
				$(pstrTarget).html(poData.result);
			}
		});
	}

	this.getRamInUse = function(pstrTarget) {
		this.request('hardware.get_ram_in_use', '', function(poData){
			if(poData && poData.success) {
				$(pstrTarget).html(poData.result);
			}
		});
	}

	this.getTotalRam = function(pstrTarget) {
		this.request('hardware.get_total_ram', '', function(poData){
			if(poData && poData.success) {
				$(pstrTarget).html(poData.result);
			}
		});
	}

	this.aptInstall = function(pstrPackageName, pfCallback) {
		this.request('software.install', '"' +encodeURI(pstrPackageName)+ '"', function(poData){
			pfCallback(poData);
		});
	}

	this.aptRemove = function(pstrPackageName, pfCallback) {
		this.request('software.remove', '"' +encodeURI(pstrPackageName)+ '"', function(poData){
			pfCallback(poData);
		});
	}

	this.aptUpdate = function(pfCallback) {
		this.request('software.update_sources', '', function(poData){
			pfCallback(poData);
		});
	}

	this.aptDistUpgrade = function(pfCallback) {
		this.request('software.dist_upgrade', '', function(poData){
			pfCallback(poData);
		});
	}

	this.addPpa = function(pstrPpa, pfCallback) {
		this.request('ppa.add', '"' +encodeURI(pstrPpa)+ '"', function(poData){
			pfCallback(poData);
		});
	}

	this.removePpa = function(pstrPpa, pfCallback) {
		this.request('ppa.remove', '"' +encodeURI(pstrPpa)+ '"', function(poData){
			pfCallback(poData);
		});
	}

	this.getActivePpas = function(pfCallback){
		this.request('ppa.get_active', '', function(poData){
			var laResult = (poData && poData.success)? poData.result : [];
			pfCallback(laResult);
		});
	}

	this.purgePpa = function(pstrPpa, pfCallback) {
		this.request('ppa.purge', '"' +encodeURI(pstrPpa)+ '"', function(poData){
			pfCallback(poData);
		});
	}

	this.shutdown = function(pfCallback) {
		this.request('ubuntu.shutdown', '', function(poData){
			return (poData && poData.success)? pfCallback(poData.success) : pfCallback(false);
		});
	}

	this.reboot = function(pfCallback) {
		this.request('ubuntu.reboot', '', function(poData){
			return (poData && poData.success)? pfCallback(poData.success) : pfCallback(false);
		});
	}

	this.installAddonRepositoryFromUrl = function(pstrUrl, pstrFileName, pfCallback){
		this.request('xbmc.install_repository', '"' +encodeURI(pstrUrl)+ '","' +encodeURI(pstrFileName)+ '"', function(poData){
			pfCallback(poData);
		});
	}

	this.backupXbmcConfig = function(pfCallback) {
		this.request('xbmc.backup_config', '', function(poData){
			return (poData && poData.success)? pfCallback(poData.success) : pfCallback(false);
		});
	}

	this.deleteBackup = function(pstrFileName, pfCallback){
		this.request('xbmc.delete_backup', '"' +encodeURI(pstrFileName)+ '"', function(poData){
			return (poData && poData.success)? pfCallback(poData.success) : pfCallback(false);
		});
	}

	this.restoreBackup = function(pstrFileName, pfCallback){
		this.request('xbmc.restore_backup', '"' +encodeURI(pstrFileName)+ '"', function(poData){
			return (poData && poData.success)? pfCallback(poData.success) : pfCallback(false);
		});
	}
}
