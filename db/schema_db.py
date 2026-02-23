from db.schema_graph import SCHEMA_GRAPH

def get_all_table_descriptions():
    descriptions = {}
    for table, info in SCHEMA_GRAPH.items():
        descriptions[table] = {
            "description": info["description"],
            "use_case": info["use_case"],
            "aliases": info["aliases"]
        }
    return descriptions

def get_table_schema(table_name: str):
    if table_name not in SCHEMA_GRAPH:
        return None
    return SCHEMA_GRAPH[table_name]

def get_column_details(table_name: str):
    if table_name not in SCHEMA_GRAPH:
        return None
    return SCHEMA_GRAPH[table_name]["columns"]

def get_cast_columns(table_name: str):
    if table_name not in SCHEMA_GRAPH:
        return []
    columns = SCHEMA_GRAPH[table_name]["columns"]
    cast_cols = []
    for col_name, col_info in columns.items():
        if col_info.get("cast_required"):
            cast_cols.append({
                "column": col_name,
                "cast_as": col_info["cast_as"]
            })
    return cast_cols