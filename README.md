This module is a prototype of a monitoring tool for a system 
continuously streaming data. It generates synthetic data (to replace
the actual system) then reads it, stores it on a SQLite database, 
produces plots and performs checks. A webserver shows the plots in a 
HTML page, that is automatically refreshed. Warning message appear in
the webpage to report malfunctioning/need for intervention.

How to execute: 

./bin/startapplication.sh 

starts the reading/analyzing script (check_data_DB.py) and the web 
server (webserver.py). How to stop: in the current version the program 
runs an infinite loop.
Both reading/analyzing script, and the web server need to be stopped.

Pandas rolling functions syntax changed after version 0.18.0. Here I am 
using a older version.

Known code limitations: 
1) several parameters are now hardcoded. In a more evolved prototype, 
 most parameters would be set through the webpage.
2) the tester needs to kill both webserver.py and check_data_DB.py; one
 could rather add start/stop buttons in the webpage
 
Known scope limitations:
the web page informs the operator, but does not do that clearly enough,
and do not say what to do in case of errors. One could 
1) make plots interactive - for example using plotly or d3.js - so for 
example can get the exact day/time the problem occurred, without 
looking into the code (or the database)
2) make buttons that stay green if all OK, turn red if problem
3) make automatic e-mail/text message notifications to inform all 
 relevant parties

 
