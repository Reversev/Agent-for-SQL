# Schema Exploration Skill

## Simplified Workflow

### 1. Get Table List
- Use `sql_db_list_tables` to view all available tables

### 2. Examine Table Structure  
- Use `sql_db_schema` to check columns, data types, primary keys
- Show minimal sample data

### 3. Identify Table Relationships
- Use `sql_db_schema` to view foreign key relationships
- Determine how related tables connect

## Simple Error Handling
- Return friendly message when table doesn't exist
- Provide similar table name suggestions