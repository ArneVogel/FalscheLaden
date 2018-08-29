/*
Just draw a border round the document.body.
*/

document.body.innerHTML += '<div id="warning" style="position:absolute;left:0px;top:0px;width:100%;height:100%;z-index:100;background:rgba(200, 0, 0, 0.5);"></div>';
document.getElementById("warning").innerHTML += '<div id="warningoptions" style="position: absolute;padding: 0px 10px 10px 10px;border-width: 4px;left: 50%;top: 50%;-webkit-transform: translate(-50%, -50%);transform: translate(-50%, -50%);background-color: lightgray;color: black;border-style: solid;border: black;"><h2>Diese Seite wurde als Fake Store identifiziert</h2><br><button onclick="window.history.back()">Zurück</button><button id="warum">Warum?</button><button id="weiter">Trotzdem Weiter</button></div>';


document.getElementById("warum").onclick = function(){var domain = window.location.hostname;domain = domain.substring(domain.lastIndexOf(".", domain.lastIndexOf(".") - 1) + 1);var win = window.open('https://www.google.com/search?q="' + domain + '"+site%3Averbraucherschutz.de+OR+site%3Awatchlist-internet.at+OR+site%3Aonlinewarnungen.de"'); win.focus();};
document.getElementById("weiter").onclick = function(){document.getElementById("warning").style.display = "none";}
//alert(window.location.hostname);
