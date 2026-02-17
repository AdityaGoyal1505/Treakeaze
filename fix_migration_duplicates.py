import os
import django
from django.db.models import Count

# Adjust this if your project structure differs
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conference_mgmt.settings")

try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    exit(1)

from conference.models import Paper

def fix_duplicates():
    print("Checking for duplicate (title, author, conference)...")
    
    # Identify groups of duplicates based on the unique constraint fields
    duplicates = Paper.objects.values('title', 'author', 'conference') \
        .annotate(count=Count('id')) \
        .filter(count__gt=1)

    total_removed = 0
    if not duplicates:
        print("No duplicates found.")
        return

    for dup in duplicates:
        print(f"Processing duplicate group: {dup}")
        
        # Get all papers matching the duplicate criteria
        papers = Paper.objects.filter(
            title=dup['title'],
            author=dup['author'],
            conference=dup['conference']
        ).order_by('id')  # Keep the one created first (lowest ID)
        
        # Keep the first one
        first = papers.first()
        
        # Delete the rest
        to_delete = papers.exclude(id=first.id)
        count = to_delete.count()
        
        print(f"Keeping ID {first.id}, deleting {count} duplicates: {[p.id for p in to_delete]}")
        to_delete.delete()
        total_removed += count

    print(f"Total duplicate papers removed: {total_removed}")

if __name__ == "__main__":
    fix_duplicates()
