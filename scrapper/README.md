# pricyfy

Simple python script for alerting user when price drops below particular level

# Requirements

- Python 3.7
- Beautiful Soup 4

# Setup

There is multiple way to setup products.

<details>
    <summary>CSV</summary>
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

</details>

<details>
    <summary>Database</summary>
    Create `products` collection with given objects:
    
    Example:
    ```
        {
            'url': "https://olx.pl/mieszkanie-asdasdasdada"
            'threshold_price': 399000.00 
        }
    ```
</details>

# Supported website

At this moment we support only particular websites listed below:

- amazon.[com/de]
- mediaexpert.pl
- olx.pl
- otodom.pl

# Run

To execute script:

```
source venv/bin/activate
pip install
python productsWatcher.py
```

Script might need write permissions in order to log product history. In order to set permissions to `logs` directory
run following command;

```
sudo chmod 775 logs/
```

## Example env

DATABASE_URL='mongodb://user:pass@localhost/dbname'
DATABASE_NAME='pricify'

# Todo

- handle multiple email receipants
- refactor watchers - extract to generic watcher

## Bugs

<details>
    <summary>None!</summary> 
    ...that I know of
</details>
