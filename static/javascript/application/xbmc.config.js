function XbmcConfig() {
    this.getAvailableRepositories = function() {
        return new Array(
            new Array('Official stable builds', 'ppa:team-xbmc/ppa'),
            new Array('Official unstable builds', 'ppa:team-xbmc/unstable'), 
            new Array('Official nightly builds', 'ppa:team-xbmc/xbmc-nightly'),
            new Array('Wsnipex nightly builds', 'ppa:wsnipex/xbmc-nightly'),
            new Array('Wsnipex xvba frodo builds', 'ppa:wsnipex/xbmc-xvba-frodo'),
            new Array('Wsnipex xvba stable regular builds', 'ppa:wsnipex/xbmc-xvba'),
            new Array('Wsnipex xvba unstable builds', 'ppa:wsnipex/xbmc-xvba-testing')
        );
    }
}
