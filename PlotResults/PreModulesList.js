function loadScript(filePath) {
    const script = document.createElement('script');
    script.src = filePath;
    script.type = "text/javascript";
    script.async = "true";
    script.charset = "UTF-8"
    document.head.appendChild(script);
}

loadScript('PlotResults/FIRSTLOOP.js');
loadScript('PlotResults/PIT.js');
loadScript('PlotResults/GPRKO.js');
loadScript('PlotResults/PSK.js');
loadScript('PlotResults/PGBOX.js');
loadScript('PlotResults/SECLOOP.js');
loadScript('PlotResults/THIRDLOOP.js');
loadScript('PlotResults/SAOT.js');
loadScript('PlotResults/REACTORSIGNALS.js');
loadScript('PlotResults/COMMONFILES.js');
loadScript('PlotResults/COMBINED.js');
loadScript('PlotResults/AEROSOL.js');

