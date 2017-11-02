[![Coverage Status](https://coveralls.io/repos/github/otrabalhador/dictable/badge.svg?branch=master)](https://coveralls.io/github/otrabalhador/dictable?branch=master)

# DicTable

Work with table-like variables in python like a charm!

### Installation
    pip install dictable

### Usage

#### Imports

```` python
from dictable import (
    DicTable,
    DicTSQL
)
````

#### Inputs

```` python
table = [
    {'city': 'Uberaba', 'happiness score': 4.5},
    {'city': 'Rio de Janeiro', 'happiness score': 5.2},
    {'city': 'Melbourne', 'happiness score': 7.1},
    {'city': 'Koh Phi Phi', 'happiness score': 6.5},
    {'city': 'Amsterdam', 'happiness score': 7.5}
]
````

```` python
tabular_table = [
    {'id': 1, 'amount':  5.5, 'operation': 'credit'},
    {'id': 2, 'amount':  10.5, 'operation': 'debit'},
    {'id': 3, 'amount':  20.2, 'operation': 'credit'},
    {'id': 4, 'amount':  40, 'operation': 'debit'},
    {'id': 5, 'amount':  50, 'operation': 'debit'},
    {'id': 6, 'amount':  1, 'operation': 'credit'},
]
````


**Get columns**

```` python
DicTable(table).columns()
> dict_keys(['happiness score', 'city'])
````

**Ordered columns**

#### Ordered columns

```` python
DicTable(table).columns(ordered=True)`
> dict_keys(['city', 'happiness score'])
````

**Distinct values**

```` python
DicTable(table).distinct_column('city')`
> ['Koh Phi Phi', 'Melbourne', 'Rio de Janeiro', 'Uberaba', 'Amsterdam']
````

```` python
DicTable(table).distinct_columns(['city', 'happiness score'])
> {'happiness score': [7.5, 4.5, 5.2, 6.5, 7.1], 'city': ['Koh Phi Phi', 'Melbourne', 'Rio de Janeiro', 'Uberaba', 'Amsterdam']}
````

**Group by**

```` python
DicTable(tabular_table).group_by(['operation'], count=True)
> [{'count': 3, 'operation': 'credit'}, {'count': 3, 'operation': 'debit'}]
````

**Group by and sum columns**

```` python
DicTable(tabular_table).summarize({'operation': ['credit', 'debit']}, ['amount'])
> [{'amount': Decimal('26.7'), 'operation': 'credit'}, {'amount': Decimal('100.5'), 'operation': 'debit'}]
````

#### Get SQL syntax
> Currently only supporting TSQL syntax

**Parse to sql select syntax**

```` python
DicTSQL(tabular_table).select_query_syntax()
````

Output:
```` sql
 SELECT 5.5 AS amount, 1 AS id, "credit" AS operation UNION ALL
 SELECT 10.5 AS amount, 2 AS id, "debit" AS operation UNION ALL
 SELECT 20.2 AS amount, 3 AS id, "credit" AS operation UNION ALL
 SELECT 40 AS amount, 4 AS id, "debit" AS operation UNION ALL
 SELECT 50 AS amount, 5 AS id, "debit" AS operation UNION ALL
 SELECT 1 AS amount, 6 AS id, "credit" AS operation
````

**Parse to sql create temp table syntax**
```` python
DicTSQL(tabular_table).create_table_syntax('data')
````

Output

```` sql
 DROP TABLE IF EXISTS #data
 SELECT
     *
 INTO #data
 FROM
     (
       SELECT 5.5 AS amount, 1 AS id, "credit" AS operation UNION ALL
       SELECT 10.5 AS amount, 2 AS id, "debit" AS operation UNION ALL
       SELECT 20.2 AS amount, 3 AS id, "credit" AS operation UNION ALL
       SELECT 40 AS amount, 4 AS id, "debit" AS operation UNION ALL
       SELECT 50 AS amount, 5 AS id, "debit" AS operation UNION ALL
       SELECT 1 AS amount, 6 AS id, "credit" AS operation
     ) data
````
