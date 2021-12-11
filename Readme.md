# Eurovat

A python library to get the vat right in the EU.

## Features

* fetch vat-rates from [tedb](https://ec.europa.eu/taxation_customs/tedb/vatSearchForm.html)
* get the proper vat-rate
    - for [cn-codes](https://ec.europa.eu/taxation_customs/business/calculation-customs-duties/customs-tariff/combined-nomenclature_en)
    - for [cpa-codes](https://ec.europa.eu/eurostat/web/cpa/cpa-2008) - UNTESTED/PARTIAL SUPPORT
    - for a given datetime (temporary vat-rates)
* VIES validation
* cn-code helpers

## Planned features

* fetch newest rates daily with gh-actions and submit automated PR's

## Historic Data

If you need historic data, you should fetch the database with the required starting date:

``` python
import eurovat
import datetime

registry = eurovat.VatRuleRegistry()
registry.date_begin = datetime.datetime(1970, 1, 1)

# This will try to write to vat_rules.json in the package directory
registry.update()

# This will update the in-memory database, all changes will be lost
registry.fetch()

# get a historic vat-rate

rate1 = registry.get_vat_rate("AT", "49020000", date=datetime.datetime(year=2019, month=10, day=5))
# rate1 = 10

rate2 = registry.get_vat_rate("AT", "49020000", date=datetime.datetime(year=2016, month=10, day=5))
# rate2 = 20
```

## Filesystem cache

when writing to package data is not an option, you can use a custom cache-file:

``` python
import eurovat
import datetime

class Registry(eurovat.VatRuleRegistry):
    cache = eurovat.FilesystemCache("/tmp/vat_rules.json")
    date_begin = datetime.datetime(1970, 1, 1)


registry = Registry()
registry.update()

```

## Custom cache

You can use a custom cache too.
Find an example in `eurovat.cache.django`

Here is how to use it:

``` python
import eurovat
import datetime

from eurovat.cache.django import DjangoCache


class Registry(eurovat.VatRuleRegistry):
    cache_factory = lambda: DjangoCache("eurovat_rates")
    date_begin = datetime.datetime(1970, 1, 1)


registry = Registry()
registry.update()

```
