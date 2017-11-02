DROP TABLE IF EXISTS #{table_name}
SELECT
    *
INTO #{table_name}
FROM
    (
        {select_statement}
    ) {table_name}
