# PostgreSQL

1. Revoke all permission from an user

```sql
REVOKE ALL ON ALL TABLES IN SCHEMA schema_name FROM user_name;
```

2. Dropping an user. Ref [https://repost.aws/knowledge-center/rds-postgresql-drop-user-role#](https://repost.aws/knowledge-center/rds-postgresql-drop-user-role#)

3. Dropping an active database

```sql
-- kill connection
SELECT pg_terminate_backend(pg_stat_activity.
 pid)
 FROM pg_stat_activity
 WHERE datname = current_database()
   AND pid <> pg_backend_pid();

-- switch database

\c postgres;

-- drop database
drop database "<db_name>" WITH (FORCE);
```
