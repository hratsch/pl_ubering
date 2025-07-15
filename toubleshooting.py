import os
import glob

# Define the project root (assuming run from project root)
project_root = os.getcwd()

# List of relevant files/paths for DB/migration troubleshooting
# To make reusable: Add more paths here as needed, e.g., 'app/routers/auth.py'
files_to_include = [
    'alembic.ini',  # Migration config
    '.env',  # WARNING: Redact secrets (e.g., passwords) before sharing output!
    '.env.example',  # Fallback if .env has secrets
    'app/config.py',
    'app/database.py',
    'migrations/env.py',
    'Makefile',
    'docker-compose.yml',  # For context, even if not using
    'app/models/base.py',
    'app/models/trip.py',
    'app/models/expense.py',
    'app/models/app_config.py',
    'app/main.py',
]

# Add all migration files dynamically
migration_files = glob.glob('migrations/versions/*.py')
files_to_include.extend(migration_files)

# Output file
output_file = 'codebase_dump.md'

with open(output_file, 'w') as out_f:
    out_f.write("# Relevant Codebase Files for Troubleshooting\n\n")
    out_f.write("This markdown contains the contents of relevant files for DB connection and migration issues. Secrets in .env should be redacted.\n\n")

    for file_path in files_to_include:
        full_path = os.path.join(project_root, file_path)
        out_f.write(f"## File: {file_path}\n\n")
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                lang = "python" if file_path.endswith('.py') else "yaml" if file_path.endswith('.yml') else "makefile" if file_path == 'Makefile' else "ini" if file_path.endswith('.ini') else "text"
                out_f.write(f"```{lang}\n")
                out_f.write(content)
                out_f.write("\n```\n\n")
            except Exception as e:
                out_f.write(f"Error reading file: {str(e)}\n\n")
        else:
            out_f.write("File not found.\n\n")

print(f"Script complete. Output saved to {output_file}. Please redact any secrets and share its content.")