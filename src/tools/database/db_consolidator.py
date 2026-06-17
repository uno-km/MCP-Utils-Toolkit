import sqlite3
import os

def _get_connection(db_path: str):
    """Safely return sqlite3 connection for the given absolute path."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    return sqlite3.connect(db_path)

def db_get_schema(db_path: str) -> str:
    """Analyze and return schemas (tables, columns, SQL definition) of the SQLite database."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        if not tables:
            conn.close()
            return f"Database at {db_path} has no tables."
            
        report = f"=== SCHEMA REPORT FOR: {db_path} ===\n\n"
        for table_name, create_sql in tables:
            report += f"Table: {table_name}\n"
            report += f"SQL definition:\n{create_sql}\n"
            
            # Fetch table info (columns, types, pk, etc.)
            cursor.execute(f"PRAGMA table_info({table_name});")
            cols = cursor.fetchall()
            report += "Columns:\n"
            for cid, name, type_name, notnull, dflt_value, pk in cols:
                pk_indicator = " [PRIMARY KEY]" if pk else ""
                nn_indicator = " [NOT NULL]" if notnull else ""
                report += f"  - {name} ({type_name}){pk_indicator}{nn_indicator}\n"
            report += "-" * 50 + "\n"
            
        conn.close()
        return report
    except Exception as e:
        return f"Error analyzing DB schema: {str(e)}"

def db_execute_query(db_path: str, query: str, read_only: bool = True) -> str:
    """Execute a SQL query/command safely. In read-only mode, only SELECT is permitted."""
    query_stripped = query.strip().upper()
    if read_only and not query_stripped.startswith("SELECT") and not query_stripped.startswith("PRAGMA") and not query_stripped.startswith("EXPLAIN"):
        return "Security Error: Writing/Modifying operations are blocked in read-only mode."
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query_stripped.startswith("SELECT") or query_stripped.startswith("PRAGMA") or query_stripped.startswith("EXPLAIN"):
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.close()
            
            if not rows:
                return f"Query executed successfully. Headers: {headers}\nResult: 0 rows returned."
                
            report = f"Headers: {headers}\n"
            for row in rows[:100]:  # Limit output
                report += f"{row}\n"
            if len(rows) > 100:
                report += f"... (truncated, total {len(rows)} rows)"
            return report
        else:
            conn.commit()
            changes = conn.changes()
            conn.close()
            return f"Command executed successfully. Database changes made: {changes} rows."
    except Exception as e:
        return f"Database Query Error: {str(e)}"

def db_merge_tables(src_db: str, dest_db: str, table_name: str, key_column: str) -> str:
    """
    Merge data from src_db.table_name into dest_db.table_name.
    Inserts missing records and updates matching records using key_column.
    """
    try:
        if not os.path.exists(src_db):
            return f"Error: Source database does not exist at {src_db}"
        if not os.path.exists(dest_db):
            return f"Error: Destination database does not exist at {dest_db}"
            
        src_conn = sqlite3.connect(src_db)
        src_cursor = src_conn.cursor()
        
        # Verify table exists in source
        src_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not src_cursor.fetchone():
            src_conn.close()
            return f"Error: Table '{table_name}' does not exist in source database."
            
        # Get column info
        src_cursor.execute(f"PRAGMA table_info({table_name});")
        src_cols = [col[1] for col in src_cursor.fetchall()]
        
        if key_column not in src_cols:
            src_conn.close()
            return f"Error: Key column '{key_column}' not found in table '{table_name}'."
            
        # Fetch all source records
        src_cursor.execute(f"SELECT * FROM {table_name};")
        records = src_cursor.fetchall()
        src_conn.close()
        
        if not records:
            return f"No records found in source table '{table_name}' to merge."
            
        dest_conn = sqlite3.connect(dest_db)
        dest_cursor = dest_conn.cursor()
        
        # Verify destination table exists; if not, create it with same schema
        dest_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not dest_cursor.fetchone():
            # Get table SQL creation script from source db
            src_conn_temp = sqlite3.connect(src_db)
            c_temp = src_conn_temp.cursor()
            c_temp.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_sql = c_temp.fetchone()[0]
            src_conn_temp.close()
            
            dest_cursor.execute(create_sql)
            dest_conn.commit()
            
        # Fetch existing keys in destination table
        dest_cursor.execute(f"SELECT {key_column} FROM {table_name};")
        dest_keys = {row[0] for row in dest_cursor.fetchall()}
        
        inserted = 0
        updated = 0
        
        # Build SQL statements
        # INSERT: INSERT INTO table (col1, col2) VALUES (?, ?)
        col_names = ", ".join(src_cols)
        placeholders = ", ".join(["?"] * len(src_cols))
        insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders});"
        
        # UPDATE: UPDATE table SET col1=?, col2=? WHERE key_column=?
        update_set = ", ".join([f"{col}=?" for col in src_cols if col != key_column])
        update_sql = f"UPDATE {table_name} SET {update_set} WHERE {key_column}=?;"
        
        key_index = src_cols.index(key_column)
        
        for record in records:
            rec_key = record[key_index]
            if rec_key in dest_keys:
                # Update (bind update columns + key column)
                update_values = [record[i] for i in range(len(src_cols)) if i != key_index] + [rec_key]
                dest_cursor.execute(update_sql, update_values)
                updated += 1
            else:
                # Insert
                dest_cursor.execute(insert_sql, record)
                inserted += 1
                
        dest_conn.commit()
        dest_conn.close()
        
        return f"Successfully merged table '{table_name}': {inserted} rows inserted, {updated} rows updated in destination DB."
    except Exception as e:
        return f"Error during DB merge operation: {str(e)}"
