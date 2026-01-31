"""
Fix script to make subreviewer_id nullable in SQLite.
SQLite doesn't support ALTER COLUMN, so we need to recreate the table.
"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("Making subreviewer_id nullable in conference_subreviewerinvite...")

# Step 1: Create new table with correct schema
cursor.execute("""
CREATE TABLE IF NOT EXISTS conference_subreviewerinvite_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email varchar(254) NOT NULL,
    status varchar(10) NOT NULL,
    requested_at datetime NOT NULL,
    responded_at datetime NULL,
    token varchar(64) NOT NULL UNIQUE,
    invited_by_id bigint NOT NULL REFERENCES auth_user(id),
    paper_id bigint NOT NULL REFERENCES conference_paper(id),
    subreviewer_id bigint NULL REFERENCES auth_user(id),
    track_id bigint NULL REFERENCES conference_track(id),
    invitee_name varchar(255) NOT NULL DEFAULT ''
)
""")

# Step 2: Copy data from old table to new
cursor.execute("""
INSERT INTO conference_subreviewerinvite_new 
    (id, email, status, requested_at, responded_at, token, invited_by_id, paper_id, subreviewer_id, track_id, invitee_name)
SELECT id, email, status, requested_at, responded_at, token, invited_by_id, paper_id, subreviewer_id, track_id, invitee_name
FROM conference_subreviewerinvite
""")

# Step 3: Drop old table
cursor.execute("DROP TABLE conference_subreviewerinvite")

# Step 4: Rename new table
cursor.execute("ALTER TABLE conference_subreviewerinvite_new RENAME TO conference_subreviewerinvite")

# Step 5: Recreate indexes
cursor.execute("CREATE INDEX IF NOT EXISTS conference_subreviewerinvite_invited_by_id ON conference_subreviewerinvite(invited_by_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS conference_subreviewerinvite_paper_id ON conference_subreviewerinvite(paper_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS conference_subreviewerinvite_subreviewer_id ON conference_subreviewerinvite(subreviewer_id)")
cursor.execute("CREATE INDEX IF NOT EXISTS conference_subreviewerinvite_track_id ON conference_subreviewerinvite(track_id)")

conn.commit()

# Verify the change
cursor.execute("PRAGMA table_info(conference_subreviewerinvite)")
print("\nNew table schema:")
for row in cursor.fetchall():
    col_name = row[1]
    col_type = row[2]
    not_null = "NOT NULL" if row[3] else "NULL"
    print(f"  {col_name}: {col_type} {not_null}")

conn.close()
print("\nDone! subreviewer_id is now nullable.")
