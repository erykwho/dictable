DROP TABLE IF EXISTS #{table_name}
SELECT
    *
INTO #{table_name}
FROM
    (
        {sub_select_statement}
    ) {table_name}
