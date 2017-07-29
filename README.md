# CryptoTracker
Monitoring CryptoCurrency exchanges to collect data for the algorithmic trading analysis. Pull Requests welcome and encouraged.

# Supported Exchanges
 1. [BitFinex](https://bitfinex.com/)
 2. [BitTrex](https://bittrex.com/)
 3. [GDAX](https://gdax.com)
 4. [Gemini](https://gemini.com)
 5. [Kraken](https://kraken.com)
 6. [Poloniex](https://poloniex.com)

# Screenshot

![Dashboard 1](./resources/img/Dashboard.png "Dashboard 1")

![Dashboard 2](./resources/img/Dashboard2.png "Dashboard 2")

# Configuration
1. Rename app/default.env to app/.env
2. Adjust timer settings in settings.py (optional)

# Running
```js
docker-compose build && docker-compose up
```
This will build then launch 3 docker containers. The first two being configurable builds Elastic Search and Kibana (customizable YML and Dockerfiles included). The third being a python2.7 container for our app which is automatically configured to run after an initial sleep timer. After the system loads, You should then be able to navigate to Kibana to see information starting to be entered into the system.

http://localhost:5601/

If this is the first time running Kibana, it may take an additional minute to load as the container runs it's initial optimization script. You will also need to add the following index patterns, with Time-field name being set to tracker_time:

```js
eth.*.ticker
*.*.ticker
```

 A json file containing saved objects and dashboards is provided under /resources. This file can be imported from Kibana's UI by navigating to Management->Saved Objects->Import. You should also configure the dashboard to auto reload.

# Production Settings
 On a live system, vm_map_max_count should be permanently set in /etc/sysctl.conf:
```js
 $ grep vm.max_map_count /etc/sysctl.conf
 vm.max_map_count=262144
```

# Additional Resources
Use resources/configure-kibana.sh to automatically set default indexes, and import saved objects.
# Powered By
<a href="http://ethventures.io/" rel="EthVentures">![EthVentures](./resources/img/ethventures-logo.png)</a>
