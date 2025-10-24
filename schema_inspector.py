import sqlite3
import json

def get_schema_report():
    try:
        conn = sqlite3.connect('monitor_ping.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        tables = cursor.fetchall()

        schema_report = {}

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            schema_report[table_name] = []
            for col in columns:
                # col is a tuple: (cid, name, type, notnull, dflt_value, pk)
                col_info = {
                    "name": col[1],
                    "type": col[2],
                    "not_null": bool(col[3]),
                    "primary_key": bool(col[5])
                }
                schema_report[table_name].append(col_info)

        conn.close()
        return schema_report

    except sqlite3.Error as e:
        return {"error": str(e)}

if __name__ == "__main__":
    report = get_schema_report()
    print(json.dumps(report, indent=4))