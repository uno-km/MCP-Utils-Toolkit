import sqlite3
import os
import re
import json
import random
from datetime import datetime

def _get_connection(db_path: str):
    """Safely return sqlite3 connection for the given absolute path."""
    # Enforce safe path validation inside C:\ameva
    normalized_path = os.path.abspath(db_path)
    if not normalized_path.lower().startswith(r"c:\ameva"):
        raise PermissionError(f"Security Error: Access to path '{normalized_path}' is denied. Only 'C:\\ameva' subfolders are allowed.")
        
    if not os.path.exists(normalized_path):
        raise FileNotFoundError(f"Database file not found at {normalized_path}")
    return sqlite3.connect(normalized_path)

def db_get_schema(db_path: str) -> str:
    """Analyze and return schemas (tables, columns, SQL definition) of the SQLite database."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        if not tables:
            conn.close()
            return f"Database at {db_path} has no tables."
            
        report = f"=== SCHEMA REPORT FOR: {db_path} ===\n\n"
        for table_name, create_sql in tables:
            report += f"Table: {table_name}\n"
            report += f"SQL definition:\n{create_sql}\n"
            
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
    """Execute a SQL query/command safely. In read-only mode, only SELECT/PRAGMA/EXPLAIN is permitted."""
    query_stripped = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL).strip().upper()
    
    if read_only:
        # Prevent any DDL or write DML
        dangerous_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "REPLACE", "RENAME", "TRUNCATE"]
        for kw in dangerous_keywords:
            if re.search(r'\b' + kw + r'\b', query_stripped):
                return f"Security Error: Writing/Modifying operation '{kw}' is blocked in read-only mode."
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        
        is_select = any(query_stripped.startswith(prefix) for prefix in ["SELECT", "PRAGMA", "EXPLAIN", "WITH"])
        if is_select:
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.close()
            
            if not rows:
                return f"Query executed successfully. Headers: {headers}\nResult: 0 rows returned."
                
            report = f"Headers: {headers}\n"
            for row in rows[:100]:
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
        # Enforce path safety
        src_db = os.path.abspath(src_db)
        dest_db = os.path.abspath(dest_db)
        if not src_db.lower().startswith(r"c:\ameva") or not dest_db.lower().startswith(r"c:\ameva"):
            return "Security Error: Both databases must be in the C:\\ameva directory."
            
        if not os.path.exists(src_db):
            return f"Error: Source database does not exist at {src_db}"
        if not os.path.exists(dest_db):
            return f"Error: Destination database does not exist at {dest_db}"
            
        src_conn = sqlite3.connect(src_db)
        src_cursor = src_conn.cursor()
        
        src_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not src_cursor.fetchone():
            src_conn.close()
            return f"Error: Table '{table_name}' does not exist in source database."
            
        src_cursor.execute(f"PRAGMA table_info({table_name});")
        src_cols = [col[1] for col in src_cursor.fetchall()]
        
        if key_column not in src_cols:
            src_conn.close()
            return f"Error: Key column '{key_column}' not found in table '{table_name}'."
            
        src_cursor.execute(f"SELECT * FROM {table_name};")
        records = src_cursor.fetchall()
        src_conn.close()
        
        if not records:
            return f"No records found in source table '{table_name}' to merge."
            
        dest_conn = sqlite3.connect(dest_db)
        dest_cursor = dest_conn.cursor()
        
        dest_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not dest_cursor.fetchone():
            src_conn_temp = sqlite3.connect(src_db)
            c_temp = src_conn_temp.cursor()
            c_temp.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_sql = c_temp.fetchone()[0]
            src_conn_temp.close()
            
            dest_cursor.execute(create_sql)
            dest_conn.commit()
            
        dest_cursor.execute(f"SELECT {key_column} FROM {table_name};")
        dest_keys = {row[0] for row in dest_cursor.fetchall()}
        
        inserted = 0
        updated = 0
        
        col_names = ", ".join(src_cols)
        placeholders = ", ".join(["?"] * len(src_cols))
        insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders});"
        
        update_set = ", ".join([f"{col}=?" for col in src_cols if col != key_column])
        update_sql = f"UPDATE {table_name} SET {update_set} WHERE {key_column}=?;"
        
        key_index = src_cols.index(key_column)
        
        for record in records:
            rec_key = record[key_index]
            if rec_key in dest_keys:
                update_values = [record[i] for i in range(len(src_cols)) if i != key_index] + [rec_key]
                dest_cursor.execute(update_sql, update_values)
                updated += 1
            else:
                dest_cursor.execute(insert_sql, record)
                inserted += 1
                
        dest_conn.commit()
        dest_conn.close()
        
        return f"Successfully merged table '{table_name}': {inserted} rows inserted, {updated} rows updated in destination DB."
    except Exception as e:
        return f"Error during DB merge operation: {str(e)}"


# ==============================================================================
# ENTERPRISE PRO FEATURES IMPLEMENTATION
# ==============================================================================

def db_generate_erd(db_path: str) -> str:
    """Generate a copy-pasteable Mermaid ER Diagram of the database schema."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        if not tables:
            conn.close()
            return "No tables found in the database to generate an ERD."
            
        erd = "erDiagram\n"
        relationships = []
        
        for table in tables:
            erd += f"    {table} {{\n"
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            
            # Get foreign keys to mark them
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fks = cursor.fetchall()
            fk_cols = {f[3]: f for f in fks if f[3]} # map child_column -> fk_info
            
            for cid, col_name, col_type, notnull, dflt, pk in cols:
                pk_flag = " PK" if pk else ""
                fk_flag = " FK" if col_name in fk_cols else ""
                # Clean type name for Mermaid compatibility
                clean_type = re.sub(r'[^a-zA-Z0-9]', '', col_type).lower() or "text"
                erd += f"        {clean_type} {col_name}{pk_flag}{fk_flag}\n"
            erd += "    }\n"
            
            # Construct relationships: child_table ||--o{ parent_table : "references"
            for fk in fks:
                # fk structure: (id, seq, table, from_col, to_col, on_update, on_delete, match)
                parent_table = fk[2]
                from_col = fk[3]
                to_col = fk[4]
                relationships.append(f"    {parent_table} ||--o{{ {table} : \"{from_col}->{to_col}\"")
                
        conn.close()
        
        erd += "\n" + "\n".join(relationships)
        return f"```mermaid\n{erd}\n```"
    except Exception as e:
        return f"Error generating Mermaid ERD: {str(e)}"


def db_generate_mock_data(db_path: str, table_name: str, count: int = 50) -> str:
    """Generate realistic mock data and populate the table automatically respecting FKs."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Verify table
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = cursor.fetchall()
        
        # Get foreign keys to resolve them dynamically
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        fks = cursor.fetchall()
        fk_map = {f[3]: f[2] for f in fks if f[3]} # col -> parent_table
        
        # Pre-fetch parent table IDs to respect FK references
        parent_data = {}
        for col_name, parent_table in fk_map.items():
            cursor.execute(f"PRAGMA table_info({parent_table});")
            parent_cols = cursor.fetchall()
            pk_col = next((c[1] for c in parent_cols if c[5]), parent_cols[0][1])
            
            cursor.execute(f"SELECT {pk_col} FROM {parent_table} LIMIT 100;")
            parent_ids = [r[0] for r in cursor.fetchall()]
            if not parent_ids:
                conn.close()
                return f"Constraint Error: Parent table '{parent_table}' has no records. Populate it first before inserting into '{table_name}'."
            parent_data[col_name] = parent_ids
            
        first_names = ["Minsoo", "Jiho", "Yeon", "Jun", "Sujin", "Sunghwan", "Hyejin", "Gildong", "Chulsoo", "Younghee"]
        last_names = ["Kim", "Lee", "Park", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim"]
        domains = ["gmail.com", "naver.com", "daum.net", "outlook.com", "yahoo.com"]
        
        inserted = 0
        col_names = [c[1] for c in cols]
        
        # Identify autoincrement integer PK to skip
        pk_col_info = next((c for c in cols if c[5]), None)
        is_integer_pk = pk_col_info and "INT" in pk_col_info[2].upper()
        
        insert_cols = [c for c in col_names if not (is_integer_pk and c == pk_col_info[1])]
        placeholders = ", ".join(["?"] * len(insert_cols))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(insert_cols)}) VALUES ({placeholders});"
        
        for i in range(count):
            row_data = []
            for col in cols:
                name = col[1]
                col_type = col[2].upper()
                is_pk = col[5]
                
                if is_integer_pk and name == pk_col_info[1]:
                    continue # Skip autoincrement
                    
                # If it's a foreign key, pull from pre-fetched parent IDs
                if name in parent_data:
                    row_data.append(random.choice(parent_data[name]))
                    continue
                    
                # Heuristic data generators
                name_lower = name.lower()
                if "email" in name_lower:
                    row_data.append(f"{random.choice(first_names).lower()}{random.randint(10,99)}@{random.choice(domains)}")
                elif "phone" in name_lower or "tel" in name_lower:
                    row_data.append(f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}")
                elif "name" in name_lower:
                    row_data.append(f"{random.choice(first_names)} {random.choice(last_names)}")
                elif "uuid" in name_lower:
                    import uuid
                    row_data.append(str(uuid.uuid4()))
                elif "date" in name_lower or "time" in name_lower or "created" in name_lower or "updated" in name_lower:
                    row_data.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                elif "status" in name_lower:
                    row_data.append(random.choice(["ACTIVE", "PENDING", "INACTIVE"]))
                elif "INT" in col_type:
                    row_data.append(random.randint(1, 10000) if not is_pk else i + 100)
                elif "REAL" in col_type or "NUM" in col_type or "FLOAT" in col_type:
                    row_data.append(round(random.uniform(10.0, 1000.0), 2))
                else:
                    row_data.append(f"MockData_{name}_{i}")
                    
            cursor.execute(insert_sql, row_data)
            inserted += 1
            
        conn.commit()
        conn.close()
        return f"Successfully generated and inserted {inserted} mock records into table '{table_name}'."
    except Exception as e:
        return f"Error generating mock data: {str(e)}"


def db_global_search_value(db_path: str, search_query: str) -> str:
    """Search for a specific string value across all text columns of all tables."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        matches = []
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            text_cols = [c[1] for c in cols if any(t in c[2].upper() for t in ["TEXT", "CHAR", "VARCHAR", "CLOB"])]
            
            if not text_cols:
                continue
                
            # Construct dynamic query
            where_clauses = " OR ".join([f"{col} LIKE ?" for col in text_cols])
            query = f"SELECT * FROM {table} WHERE {where_clauses};"
            
            params = [f"%{search_query}%"] * len(text_cols)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if rows:
                for row in rows[:10]: # Cap per table to avoid flooding
                    matches.append(f"Table: {table} | Row: {row}")
                if len(rows) > 10:
                    matches.append(f"Table: {table} | ... and {len(rows)-10} more matches.")
                    
        conn.close()
        if not matches:
            return f"No matches found for search query '{search_query}'."
        return f"=== GLOBAL SEARCH RESULTS FOR '{search_query}' ===\n\n" + "\n".join(matches)
    except Exception as e:
        return f"Error during global search: {str(e)}"


def db_transpile_sqlite_to_other(db_path: str, target_dialect: str) -> str:
    """Transpile SQLite schema and data into PostgreSQL or MySQL DDL/DML script."""
    target_dialect = target_dialect.lower()
    if target_dialect not in ["postgresql", "mysql"]:
        return "Error: Target dialect must be either 'postgresql' or 'mysql'."
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        sql_script = f"-- Generated Migration Script for {target_dialect.upper()}\n"
        sql_script += f"-- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for table_name, create_sql in tables:
            # Transpile create table
            new_ddl = create_sql
            if target_dialect == "postgresql":
                # Convert INTEGER PRIMARY KEY AUTOINCREMENT -> SERIAL PRIMARY KEY
                new_ddl = re.sub(
                    r'(?i)\bINTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT\b', 
                    'SERIAL PRIMARY KEY', 
                    new_ddl
                )
                # Double quotes for table and column names to respect keywords if needed
                new_ddl = new_ddl.replace('"', '') # Clean first
            elif target_dialect == "mysql":
                # Convert AUTOINCREMENT -> AUTO_INCREMENT
                new_ddl = re.sub(
                    r'(?i)\bAUTOINCREMENT\b', 
                    'AUTO_INCREMENT', 
                    new_ddl
                )
                
            sql_script += f"{new_ddl};\n\n"
            
            # Fetch and dump data
            cursor.execute(f"PRAGMA table_info({table_name});")
            cols = [c[1] for c in cursor.fetchall()]
            
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            if rows:
                sql_script += f"-- Data insertion for {table_name}\n"
                col_str = ", ".join(cols)
                for row in rows:
                    val_list = []
                    for v in row:
                        if v is None:
                            val_list.append("NULL")
                        elif isinstance(v, (int, float)):
                            val_list.append(str(v))
                        else:
                            # Escape single quotes
                            escaped = str(v).replace("'", "''")
                            val_list.append(f"'{escaped}'")
                    val_str = ", ".join(val_list)
                    sql_script += f"INSERT INTO {table_name} ({col_str}) VALUES ({val_str});\n"
                sql_script += "\n"
                
        conn.close()
        return sql_script
    except Exception as e:
        return f"Error transpiling SQLite to {target_dialect}: {str(e)}"


def db_profile_and_scan_health(db_path: str) -> str:
    """Analyze indices, scan orphaned rows (FK breaks), check high NULL rates, detect numeric outliers."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [r[0] for r in cursor.fetchall()]
        
        report = f"=== DATABASE HEALTH & ANOMALY REPORT ===\n\n"
        
        # 1. Check duplicate indexes
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
        indices = cursor.fetchall()
        idx_info = {}
        for idx_name, tbl_name in indices:
            cursor.execute(f"PRAGMA index_info({idx_name});")
            columns = [r[2] for r in cursor.fetchall()]
            key = (tbl_name, tuple(columns))
            if key in idx_info:
                idx_info[key].append(idx_name)
            else:
                idx_info[key] = [idx_name]
                
        dup_indices = {k: v for k, v in idx_info.items() if len(v) > 1}
        report += "1. Duplicate Index Check:\n"
        if dup_indices:
            for (tbl, cols), names in dup_indices.items():
                report += f"  - WARNING: Table '{tbl}' has duplicate indexes {names} covering columns {cols}.\n"
        else:
            report += "  - OK: No duplicate indexes found.\n"
        report += "\n"
        
        # 2. Check Orphan Foreign Keys (FK validation)
        report += "2. Referential Integrity / Orphan Row Check:\n"
        orphans_found = False
        for table in tables:
            cursor.execute(f"PRAGMA foreign_key_list({table});")
            fks = cursor.fetchall()
            for fk in fks:
                parent_table = fk[2]
                child_col = fk[3]
                parent_col = fk[4] or "id" # default pk fallback
                
                # Scan for orphans: child rows whose FK points to non-existent parent PK
                query = f"SELECT COUNT(*) FROM {table} WHERE {child_col} NOT IN (SELECT {parent_col} FROM {parent_table}) AND {child_col} IS NOT NULL;"
                cursor.execute(query)
                orphans = cursor.fetchone()[0]
                if orphans > 0:
                    report += f"  - DANGER: Table '{table}' has {orphans} orphan records violating foreign key reference to {parent_table}({parent_col})!\n"
                    orphans_found = True
        if not orphans_found:
            report += "  - OK: No orphan records found. Referential integrity intact.\n"
        report += "\n"
        
        # 3. Scan high NULL rates and Numeric Outliers
        report += "3. Columns Data Profiling & Anomalies:\n"
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            total_rows = cursor.fetchone()[0]
            if total_rows == 0:
                report += f"  - Table '{table}': Empty table.\n"
                continue
                
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            for cid, col_name, col_type, notnull, dflt, pk in cols:
                # NULL Rate
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} IS NULL;")
                nulls = cursor.fetchone()[0]
                null_rate = (nulls / total_rows) * 100
                if null_rate > 50:
                    report += f"  - WARNING: Table '{table}' column '{col_name}' has a high NULL rate of {null_rate:.1f}%.\n"
                    
                # Numeric Outliers (using 3-sigma rule: values exceeding mean + 3*stddev)
                if any(t in col_type.upper() for t in ["INT", "REAL", "NUM", "FLOAT", "DOUBLE"]):
                    # Calculate mean & stddev
                    cursor.execute(f"SELECT AVG({col_name}), AVG({col_name}*{col_name}) FROM {table} WHERE {col_name} IS NOT NULL;")
                    stats = cursor.fetchone()
                    if stats and stats[0] is not None:
                        avg = stats[0]
                        variance = max(0, stats[1] - (avg * avg))
                        stddev = variance ** 0.5
                        
                        if stddev > 0:
                            upper_limit = avg + (3 * stddev)
                            lower_limit = avg - (3 * stddev)
                            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} > ? OR {col_name} < ?;", (upper_limit, lower_limit))
                            outliers = cursor.fetchone()[0]
                            if outliers > 0:
                                report += f"  - INFO: Table '{table}' column '{col_name}' has {outliers} potential statistical outliers (> 3 stddev).\n"
                                
        conn.close()
        return report
    except Exception as e:
        return f"Error executing database health check: {str(e)}"


def db_format_sql(query: str) -> str:
    """Beautify, uppercase keywords, and format raw SQL string into pretty, readable SQL."""
    # List of common SQL keywords to uppercase
    keywords = [
        r"\bselect\b", r"\bfrom\b", r"\bwhere\b", r"\bjoin\b", r"\bleft\b", r"\bright\b", r"\bouter\b",
        r"\binner\b", r"\bon\b", r"\bgroup\b", r"\bby\b", r"\border\b", r"\bhaving\b", r"\blimit\b",
        r"\band\b", r"\bor\b", r"\bas\b", r"\bin\b", r"\bis\b", r"\bnull\b", r"\bcreate\b", r"\btable\b",
        r"\binsert\b", r"\binto\b", r"\bvalues\b", r"\bupdate\b", r"\bset\b", r"\bdelete\b"
    ]
    
    formatted = query.strip()
    
    # Capitalize keywords
    for kw in keywords:
        formatted = re.sub(kw, lambda m: m.group(0).upper(), formatted, flags=re.IGNORECASE)
        
    # Standard format: Insert line breaks before major query statements
    major_clauses = ["FROM", "WHERE", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "JOIN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "SET", "VALUES"]
    for clause in major_clauses:
        # Avoid double line breaks if already formatted
        formatted = re.sub(r'\s+\b' + clause + r'\b', f'\n{clause}', formatted)
        
    # Indent elements inside parenthesis slightly (basic nesting heuristic)
    return formatted


def db_compare_schemas(src_db: str, dest_db: str) -> str:
    """Compare src_db schema to dest_db and generate missing table/column DDL sync scripts."""
    try:
        src_db = os.path.abspath(src_db)
        dest_db = os.path.abspath(dest_db)
        if not src_db.lower().startswith(r"c:\ameva") or not dest_db.lower().startswith(r"c:\ameva"):
            return "Security Error: Both databases must be in the C:\\ameva directory."
            
        src_conn = sqlite3.connect(src_db)
        src_cursor = src_conn.cursor()
        dest_conn = sqlite3.connect(dest_db)
        dest_cursor = dest_conn.cursor()
        
        # Get schemas
        src_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        src_tables = {r[0]: r[1] for r in src_cursor.fetchall()}
        
        dest_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        dest_tables = {r[0] for r in dest_cursor.fetchall()}
        
        diff_script = f"-- Schema Sync Script: {dest_db} -> match {src_db}\n\n"
        changes_detected = False
        
        # 1. Find missing tables in target
        for table, create_sql in src_tables.items():
            if table not in dest_tables:
                diff_script += f"-- Table '{table}' is missing in target. Creating...\n"
                diff_script += f"{create_sql};\n\n"
                changes_detected = True
                
        # 2. Find missing columns in target tables
        for table, create_sql in src_tables.items():
            if table in dest_tables:
                src_cursor.execute(f"PRAGMA table_info({table});")
                src_cols = {r[1]: (r[2], r[3], r[4]) for r in src_cursor.fetchall()} # name -> (type, notnull, default)
                
                dest_cursor.execute(f"PRAGMA table_info({table});")
                dest_cols = {r[1] for r in dest_cursor.fetchall()}
                
                for col_name, (col_type, notnull, default) in src_cols.items():
                    if col_name not in dest_cols:
                        diff_script += f"-- Column '{col_name}' is missing in target table '{table}'. Adding...\n"
                        notnull_str = " NOT NULL" if notnull else ""
                        dflt_str = f" DEFAULT {default}" if default is not None else ""
                        diff_script += f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}{notnull_str}{dflt_str};\n"
                        changes_detected = True
                diff_script += "\n"
                
        src_conn.close()
        dest_conn.close()
        
        if not changes_detected:
            return "No schema differences detected between source and destination databases."
            
        return diff_script
    except Exception as e:
        return f"Error during schema comparison: {str(e)}"


def db_mask_table_data(db_path: str, table_name: str, mask_rules_json: str) -> str:
    """Mask sensitive columns inside a table based on GDPR-compliant rules."""
    try:
        rules = json.loads(mask_rules_json) # {"email": "mask_email", "name": "mask_name"}
    except Exception as e:
        return f"Error: Invalid mask_rules_json format: {str(e)}"
        
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Verify table
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_cols = [c[1] for c in cursor.fetchall()]
        
        # Validate rule columns
        for col in rules.keys():
            if col not in table_cols:
                conn.close()
                return f"Error: Column '{col}' not found in table '{table_name}'."
                
        # Fetch rows
        cursor.execute(f"SELECT rowid, * FROM {table_name};")
        rows = cursor.fetchall()
        
        updated = 0
        for row in rows:
            rowid = row[0]
            # Map column name to index (shifted by 1 due to rowid)
            row_dict = {table_cols[i]: row[i+1] for i in range(len(table_cols))}
            
            update_clauses = []
            params = []
            
            for col, rule in rules.items():
                val = row_dict[col]
                if val is None:
                    continue
                    
                val_str = str(val)
                masked_val = val_str
                
                # Apply masking heuristics
                if rule == "mask_email":
                    if "@" in val_str:
                        local, domain = val_str.split("@", 1)
                        masked_local = local[0] + "***" if len(local) > 1 else local + "***"
                        masked_val = f"{masked_local}@{domain}"
                elif rule == "mask_name":
                    if len(val_str) >= 3:
                        masked_val = val_str[0] + "*" + val_str[2:]
                    elif len(val_str) == 2:
                        masked_val = val_str[0] + "*"
                    else:
                        masked_val = "*"
                elif rule == "mask_phone":
                    # Mask middle 4 numbers of 010-1234-5678 or similar
                    clean_phone = re.sub(r'[^0-9]', '', val_str)
                    if len(clean_phone) >= 10:
                        masked_val = f"{val_str[:3]}-****-{val_str[-4:]}"
                    else:
                        masked_val = "***-***-****"
                elif rule == "mask_hash":
                    import hashlib
                    masked_val = hashlib.sha256(val_str.encode()).hexdigest()[:16]
                else:
                    masked_val = "******"
                    
                update_clauses.append(f"{col}=?")
                params.append(masked_val)
                
            if update_clauses:
                params.append(rowid)
                query = f"UPDATE {table_name} SET {', '.join(update_clauses)} WHERE rowid=?;"
                cursor.execute(query, params)
                updated += 1
                
        conn.commit()
        conn.close()
        return f"Successfully masked data for {updated} rows in table '{table_name}'."
    except Exception as e:
        return f"Error masking table data: {str(e)}"


def db_optimize_query_tuning(db_path: str, slow_query: str) -> str:
    """Analyze query plan via EXPLAIN QUERY PLAN and output missing index recommendations."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Analyze using EXPLAIN QUERY PLAN
        explain_query = f"EXPLAIN QUERY PLAN {slow_query}"
        cursor.execute(explain_query)
        plan_rows = cursor.fetchall()
        
        recommendations = []
        tuning_report = "=== SQL QUERY PLAN ANALYSIS ===\n\n"
        
        for row in plan_rows:
            # Plan format: (selectid, order, from, detail)
            detail = row[3]
            tuning_report += f"Plan detail: {detail}\n"
            
            # Check for Table Scans (SCAN TABLE) which indicates no index used
            if "SCAN TABLE" in detail:
                match = re.search(r'SCAN TABLE (\w+)', detail)
                if match:
                    table_name = match.group(1)
                    
                    # Try to extract search condition columns for that table from query
                    # Look in WHERE clause for columns relating to this table
                    where_match = re.search(r'(?i)WHERE\s+(.*)', slow_query)
                    candidate_cols = []
                    if where_match:
                        where_clause = where_match.group(1)
                        # Find identifiers comparing to table columns
                        # e.g., table.col = ? or col = ?
                        # Basic regex helper
                        cols_in_where = re.findall(r'\b(?:' + table_name + r'\.)?(\w+)\s*[=<>!]+', where_clause)
                        candidate_cols.extend([c for c in cols_in_where if c.lower() not in ["null", "true", "false"]])
                        
                    # Remove duplicates while keeping order
                    seen = set()
                    candidate_cols = [c for c in candidate_cols if not (c in seen or seen.add(c))]
                    
                    if candidate_cols:
                        cols_str = ", ".join(candidate_cols)
                        idx_name = f"idx_{table_name}_{'_'.join(candidate_cols)}"
                        recommendations.append(f"CREATE INDEX {idx_name} ON {table_name}({cols_str});")
                    else:
                        recommendations.append(f"-- Suggestion: Analyze table '{table_name}' and create index on columns used in filtering/joining.")
                        
        conn.close()
        
        if recommendations:
            tuning_report += "\n=== INDEX OPTIMIZATION RECOMMENDATIONS ===\n"
            tuning_report += "\n".join(recommendations)
        else:
            tuning_report += "\n=== INDEX OPTIMIZATION RECOMMENDATIONS ===\n- OK: Query is already optimized and utilizes indices efficiently."
            
        return tuning_report
    except Exception as e:
        return f"Error during query optimization analysis: {str(e)}"


def db_enable_time_travel(db_path: str, table_name: str) -> str:
    """Enable time travel audit log shadow table and triggers for mutating operations."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        # Verify table
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if not cursor.fetchone():
            conn.close()
            return f"Table '{table_name}' does not exist."
            
        # Get columns to build JSON formatters
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        ledger_table = f"{table_name}_ledger"
        
        # Create Ledger Table
        create_ledger_sql = f"""
        CREATE TABLE IF NOT EXISTS {ledger_table} (
            ledger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            row_id INTEGER,
            operation TEXT,
            old_data TEXT,
            new_data TEXT,
            changed_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        );
        """
        cursor.execute(create_ledger_sql)
        
        # Generate JSON construction parts for OLD and NEW rows
        # SQLite json_object('col1', OLD.col1, 'col2', OLD.col2)
        old_json = "json_object(" + ", ".join([f"'{c}', OLD.{c}" for c in cols]) + ")"
        new_json = "json_object(" + ", ".join([f"'{c}', NEW.{c}" for c in cols]) + ")"
        
        # Drop existing triggers if any to prevent conflicts
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_insert;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_update;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_delete;")
        
        # 1. Trigger Insert
        trg_insert = f"""
        CREATE TRIGGER trg_{table_name}_insert AFTER INSERT ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (NEW.rowid, 'INSERT', NULL, {new_json});
        END;
        """
        
        # 2. Trigger Update
        trg_update = f"""
        CREATE TRIGGER trg_{table_name}_update AFTER UPDATE ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (NEW.rowid, 'UPDATE', {old_json}, {new_json});
        END;
        """
        
        # 3. Trigger Delete
        trg_delete = f"""
        CREATE TRIGGER trg_{table_name}_delete AFTER DELETE ON {table_name}
        BEGIN
            INSERT INTO {ledger_table} (row_id, operation, old_data, new_data)
            VALUES (OLD.rowid, 'DELETE', {old_json}, NULL);
        END;
        """
        
        cursor.execute(trg_insert)
        cursor.execute(trg_update)
        cursor.execute(trg_delete)
        
        conn.commit()
        conn.close()
        return f"Successfully enabled Time-Travel Audit on table '{table_name}'. Shadow ledger '{ledger_table}' and triggers are active."
    except Exception as e:
        return f"Error enabling time travel: {str(e)}"


def db_restore_time_travel(db_path: str, table_name: str, target_timestamp: str) -> str:
    """Restore table data back to a specific timestamp by executing mutations in reverse."""
    try:
        conn = _get_connection(db_path)
        cursor = conn.cursor()
        
        ledger_table = f"{table_name}_ledger"
        
        # Verify ledger table
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{ledger_table}';")
        if not cursor.fetchone():
            conn.close()
            return f"Time travel ledger '{ledger_table}' does not exist. Enable it first using db_enable_time_travel."
            
        # Get column definitions of target table to insert correctly
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        
        # Find PK column to match updates
        cursor.execute(f"PRAGMA table_info({table_name});")
        pk_col = next((c[1] for c in cursor.fetchall() if c[5]), None)
        
        # Temporarily disable triggers on target table to avoid logging the restore itself
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_insert;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_update;")
        cursor.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_delete;")
        
        # Fetch ledger entries since target_timestamp in REVERSE chronological order
        cursor.execute(f"SELECT operation, row_id, old_data, new_data, ledger_id FROM {ledger_table} WHERE changed_at > ? ORDER BY ledger_id DESC;", (target_timestamp,))
        ledger_rows = cursor.fetchall()
        
        if not ledger_rows:
            # Restore triggers before returning
            conn.close()
            db_enable_time_travel(db_path, table_name)
            return f"No changes detected since timestamp '{target_timestamp}'. Database is already at this state."
            
        restored_count = 0
        
        for op, row_id, old_data_json, new_data_json, ledger_id in ledger_rows:
            if op == "INSERT":
                # To reverse an INSERT, delete the row
                cursor.execute(f"DELETE FROM {table_name} WHERE rowid=?;", (row_id,))
            elif op == "DELETE":
                # To reverse a DELETE, insert the OLD data back
                old_data = json.loads(old_data_json)
                col_names = ", ".join(old_data.keys())
                placeholders = ", ".join(["?"] * len(old_data))
                vals = list(old_data.values())
                cursor.execute(f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders});", vals)
            elif op == "UPDATE":
                # To reverse an UPDATE, apply the OLD data state
                old_data = json.loads(old_data_json)
                set_clause = ", ".join([f"{k}=?" for k in old_data.keys()])
                vals = list(old_data.values())
                
                # Try using PK if exists, otherwise fall back to rowid (rowid might change on restore-inserts, so pk is preferred)
                if pk_col and pk_col in old_data:
                    pk_val = old_data[pk_col]
                    vals.append(pk_val)
                    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {pk_col}=?;", vals)
                else:
                    vals.append(row_id)
                    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE rowid=?;", vals)
                    
            restored_count += 1
            
        # Clear ledger records that have been undone
        cursor.execute(f"DELETE FROM {ledger_table} WHERE changed_at > ?;", (target_timestamp,))
        
        conn.commit()
        conn.close()
        
        # Re-enable triggers
        db_enable_time_travel(db_path, table_name)
        
        return f"Successfully restored '{table_name}' back to '{target_timestamp}'. Undid {restored_count} database mutations."
    except Exception as e:
        # Re-enable triggers on error
        try:
            db_enable_time_travel(db_path, table_name)
        except:
            pass
        return f"Error during time-travel restore operation: {str(e)}"
