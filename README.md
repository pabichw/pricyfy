# pricyfy
Simple python script for alerting user when amazon price drops below some level


# Requirements
- Python 3.7 (3.5?)
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

# Run
To lunch execute script:
```
python3.7 productsWatcher.py
```