#!/usr/bin/env python3
"""
Git Push Automation Script

This script automates the common git workflow:
1. Add all changes
2. Commit with a message
3. Push to remote repository

Usage:
    python push.py "Your commit message here"
    python push.py  # Uses default message if none provided
"""

import subprocess
import sys
import os
from datetime import datetime

def run_git_command(command):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    # Get commit message from command line argument or use default
    if len(sys.argv) > 1:
        commit_message = sys.argv[1]
    else:
        # Use timestamp as default message
        commit_message = f"Update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print("🚀 Starting git push automation...")
    print(f"📝 Commit message: '{commit_message}'")

    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Error: Not in a git repository!")
        sys.exit(1)

    # Step 1: Add all changes
    print("\n📋 Step 1: Adding all changes...")
    success, output = run_git_command('git add .')
    if success:
        print("✅ Changes added successfully")
    else:
        print(f"❌ Failed to add changes: {output}")
        sys.exit(1)

    # Step 2: Check if there are changes to commit
    success, output = run_git_command('git diff --cached --quiet')
    if success:
        print("ℹ️  No changes to commit")
        return

    # Step 3: Commit changes
    print("\n💾 Step 2: Committing changes...")
    commit_command = f'git commit -m "{commit_message}"'
    success, output = run_git_command(commit_command)
    if success:
        print("✅ Changes committed successfully")
        print(f"📊 {output.strip()}")
    else:
        print(f"❌ Failed to commit changes: {output}")
        sys.exit(1)

    # Step 4: Push to remote
    print("\n⬆️  Step 3: Pushing to remote...")
    success, output = run_git_command('git push')
    if success:
        print("✅ Changes pushed to remote successfully")
        print(f"📊 {output.strip()}")
    else:
        print(f"❌ Failed to push changes: {output}")
        sys.exit(1)

    print("\n🎉 Git push completed successfully!")

if __name__ == "__main__":
    main()