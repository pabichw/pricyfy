# pricyfy
Simple python script for alerting user when price drops below some level

# Requirements
- Python 3.7 
- Beautiful Soup 4

# Setup
Configure `products.csv` file in your root directory by adding products and their links. Format is:
```
[link] [price]
[link] [price]
[link] [price]
```

Example below:
```
https://www.amazon.de/-/pl/dp/B07W13KJZC/r 300.00
https://www.amazon.de/-/pl/dp/B07WKNQ8JT/r 300.00
```

# Supported websited
At this moment we support only particular websites listed below:
* amazon.[com/de]
* mediaexpert.pl
* otodom.pl

# Run
To execute script:

```
source env/bin/activate
pip install
python productsWatcher.py
```

Script might need write permissions in order to log product history. In order to set permissions to `logs` directory
run following command;

```
sudo chmod 775 logs/
```
