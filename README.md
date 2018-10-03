![alt text](https://i.imgur.com/Wi6F8GZ.png)

This program was created for demonstration and partial automation of Komodo GatewaysCC stack. (AssetsCC, OraclesCC, GatewaysCC, oraclesfeed dAPP)

Python3 required for execution:
`sudo apt-get install python3.6`

System have to know path to komodod. e.g.:
`export PATH=$PATH:~/komodo/src`

Before execution be sure than daemon for needed AC up.

At the moment raw version of manual gateway how-to guide can be found here: http://pad.supernet.org/cc_gateways_guide
I advice to read it before you start use this tool to understand the flow.

To start use GatewaysCC TUI:

0) `sudo apt-get install python3.6 && export PATH=$PATH:~/komodo/src` 
1) `https://github.com/tonymorony/cryptoconditions_tui`
2) `cd cryptoconditions_tui`
3) `./gateways_cc_cli.py`

-------------------------------------------------------
