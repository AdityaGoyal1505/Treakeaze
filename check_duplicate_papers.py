"""
Script to check for duplicate paper submissions before applying database constraints.
Run this before making migrations to identify potential issues.
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conference_mgmt.settings')
django.setup()

from django.db.models import Count
from conference.models import Paper

def check_duplicates():
    """Check for duplicate papers (same title, author, and conference)"""
    
    # Find papers with duplicate combinations
    duplicates = Paper.objects.values('title', 'author', 'conference').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    if not duplicates.exists():
        print("✓ No duplicate papers found. Safe to proceed with migration.")
        return True
    
    print(f"⚠ Found {duplicates.count()} sets of duplicate papers:\n")
    
    for dup in duplicates:
        papers = Paper.objects.filter(
            title=dup['title'],
            author_id=dup['author'],
            conference_id=dup['conference']
        ).order_by('submitted_at')
        
        print(f"Title: {dup['title']}")
        print(f"Author ID: {dup['author']}")
        print(f"Conference ID: {dup['conference']}")
        print(f"Number of duplicates: {dup['count']}")
        print("Papers:")
        
        for idx, paper in enumerate(papers, 1):
            print(f"  {idx}. Paper ID: {paper.paper_id}, Submitted: {paper.submitted_at}, Status: {paper.status}")
        
        print("\n" + "="*80 + "\n")
    
    print("⚠ Action Required:")
    print("Please review and manually delete duplicate papers before applying the migration.")
    print("Keep the earliest submission or the one with the most complete information.")
    return False

if __name__ == '__main__':
    check_duplicates()
