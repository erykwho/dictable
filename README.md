### Installation
    pip install dict-table

### Usage

```python
from dict_table import table

my_list = [
    {
        'column_1': 1,
        'column_2': 2,
    },
    {
        'column_1': 3,
        'column_2': 4,
    },
]
my_table = table.DictTable(my_list)
```