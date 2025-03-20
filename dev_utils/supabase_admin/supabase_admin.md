# Supabase Development Utilities

This directory contains development utilities for managing and exploring my Supabase database.

##  Usage

Each time you use this script:

1. Navigate to the dev_utils directory:
   ```bash
   cd dev_utils
   ```

2. Activate the existing virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Run commands using the script. Here are some examples:

   ```bash
   # Create a new conversation
   python supabase_admin/supabase_admin.py create conversations --data '{"user_id": "user-uuid", "title": "New Conversation"}'

   # Read a specific conversation
   python supabase_admin/supabase_admin.py read conversations --id "conversation-uuid"

   # Read all conversations (limited to 5)
   python supabase_admin/supabase_admin.py read-all conversations --limit 5

   # Update a conversation
   python supabase_admin/supabase_admin.py update conversations --id "conversation-uuid" --data '{"title": "Updated Title"}'

   # Delete a conversation
   python supabase_admin/supabase_admin.py delete conversations --id "conversation-uuid"

   # Alter table structure examples
   python supabase_admin/supabase_admin.py alter users --operation add --column nickname --type text --nullable
   python supabase_admin/supabase_admin.py alter products --operation drop --column old_field
   python supabase_admin/supabase_admin.py alter orders --operation modify --column status --type varchar --default 'pending'
   ```

## Available Commands

The script supports the following commands:

- `create <table>` --data '<json>': Create a new record
- `read <table>` --id '<uuid>': Read a single record
- `read-all <table>` [--limit N]: Read multiple records
- `update <table>` --id '<uuid>' --data '<json>': Update a record
- `delete <table>` --id '<uuid>': Delete a record
- `alter <table>` --operation <add|drop|modify> --column <name> [--type <type>] [--nullable] [--default <value>]: Alter table structure

## Important Notes

1. The script uses the Supabase service role key which has full database access
2. Credentials are loaded from the `.env` file in the dev_utils directory
3. Always use the virtual environment to ensure correct dependencies
4. JSON data must be properly escaped when passed as command-line arguments
5. Be cautious when using delete operations as they cannot be undone


## On Completion

When you're done:
1. Deactivate the virtual environment: `deactivate`
2. Return to the project root: `cd ..`
3. If any tables were added or their schemas changed, make necessary changes to app/schemas.py