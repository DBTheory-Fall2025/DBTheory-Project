def generate_schema_diagram(schemas):
    """
    Generates a Mermaid classDiagram string from the given schemas.
    
    Args:
        schemas: A dict of {db_name: schema_dict} where schema_dict is returned by get_enhanced_schema
        
    Returns:
        A string containing the Mermaid diagram definition
    """
    lines = ["classDiagram"]
    
    for db_name, schema in schemas.items():
        # Sanitize db name for namespace
        clean_db_name = db_name.replace(" ", "_").replace("-", "_")
        
        lines.append(f"    namespace {clean_db_name} {{")
        
        for table_name, details in schema.items():
            # Sanitize table name
            clean_table_name = table_name.replace(" ", "_").replace("-", "_")
            
            lines.append(f"        class {clean_table_name} {{")
            
            # Sort columns to put PKs first
            columns = list(details["columns"].items())
            pks = set(details["pks"])
            
            # Custom sort: PKs first, then others
            columns.sort(key=lambda x: 0 if x[0] in pks else 1)
            
            for col_name, dtype in columns:
                # Check markers
                markers = []
                
                if col_name in pks:
                    # Add (PK) suffix for Primary Key
                    lines.append(f"            {dtype} {col_name} (PK)")
                
                elif any(fk["col"] == col_name for fk in details["fks"]):
                    # Add (FK) suffix for Foreign Key
                    lines.append(f"            {dtype} {col_name} (FK)")
                else:
                    # Normal column
                    lines.append(f"            {dtype} {col_name}")
                
            lines.append("        }")

        lines.append("    }")
        
        # Add relationships for this DB
        for table_name, details in schema.items():
            clean_table_name = table_name.replace(" ", "_").replace("-", "_")
            
            for fk in details['fks']:
                ref_table = fk['ref_table']
                clean_ref_table = ref_table.replace(" ", "_").replace("-", "_")
                
                # Check if ref table exists in this DB schema to draw the arrow
                if ref_table in schema:
                    lines.append(f"    {clean_db_name}.{clean_table_name} --> {clean_db_name}.{clean_ref_table} : FK")

    return "\n".join(lines)
