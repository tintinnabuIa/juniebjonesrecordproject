psql -U bells -d juniebjonesrecordproject <<'SQL'
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT c.table_schema, c.table_name, c.column_name
        FROM information_schema.columns c
        LEFT JOIN information_schema.key_column_usage k
            ON c.table_name = k.table_name
            AND c.column_name = k.column_name
            AND c.table_schema = k.table_schema
        WHERE c.table_schema='public'
          AND k.column_name IS NULL
    LOOP
        EXECUTE format(
            'ALTER TABLE %I.%I ALTER COLUMN %I DROP NOT NULL;',
            r.table_schema, r.table_name, r.column_name
        );
    END LOOP;
END $$;
SQL