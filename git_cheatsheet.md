# Git Collaboration Guide for WhatsEvent Hackathon

## Quick Workflow Summary

1. **Stay Updated:**
   - Pull the latest changes before starting work:
     ```sh
     git pull origin main
     ```

2. **Create a Branch:**
   - Create a new branch for each feature:
     ```sh
     git checkout -b feature/your-feature-name
     ```

3. **Make Changes:**
   - Edit files and stage your changes:
     ```sh
     git add <files>  # or git add .
     ```
   - Commit your changes:
     ```sh
     git commit -m "Description of changes"
     ```

4. **Push Changes:**
   - Push your branch to GitHub:
     ```sh
     git push origin feature/your-feature-name
     ```

5. **Create Pull Request (PR):**
   - On GitHub, create a PR from your branch and request a review.

6. **Resolve Conflicts:**
   - If merge conflicts occur, resolve them on GitHub via the **Pull Request Merge Conflict Editor** or locally.

7. **Merge and Cleanup:**
   - Once a feature branch is merged into `main`, update your local system and delete the branch:
     ```sh
     git checkout main
     git pull origin main
      ```
     ```sh
     git branch -d <your_branch_name_here>  # Delete local branch
     ```
     ```sh
     git push origin --delete <your_branch_name_here>  # Delete remote branch
     ```
     ```sh
     git fetch --prune  # Clean up remote-tracking branches
     ```

---

Welcome to the WhatsEvent project!

This guide outlines best practices for using Git effectively during our hackathon. Follow these steps to maintain a structured workflow and prevent conflicts.

---

## 1. Staying Updated Before Starting

### Pull the Latest Changes

Before beginning any work, ensure your local repository is up to date:

```sh
cd WhatsEvent
git pull origin main
```

---

## 2. Branching Strategy

### Never Work Directly on `main`

- The `main` branch should always represent a stable version of the project.
- Always create a new branch for each feature or task.

### Creating a Feature Branch

Use descriptive branch names:

```sh
git checkout -b feature/your-feature-name  # Example: feature/add-event-form
```

---

## 3. Making Changes and Committing

### Make Your Code Changes

Edit the necessary files for your feature.

### Stage Your Changes

Add modified files:

```sh
git add <file1> <file2>  # Add specific files
git add .  # Add all changed files
```

### Commit Your Changes

Write clear and concise commit messages:

```sh
git commit -m "Add event form to UI"
```

Describe what you changed and why.

---

## 4. Pushing and Pull Requests (PRs)

### Push Your Branch

Push your branch to the remote repository:

```sh
git push origin feature/your-feature-name
```

### Create a Pull Request (PR)

1. Go to the WhatsEvent repository on GitHub.
2. Click the prompt to create a new pull request.
3. Write a clear description of your changes.
4. Request a review from a team member.

---

## 5. Resolving Conflicts and Merging

### Resolving Conflicts (If Any)

- If a merge conflict occurs, GitHub will notify you when attempting to merge a pull request.
- Conflicts can be resolved directly on GitHub via the **Pull Request Merge Conflict Editor**.
- If you prefer to resolve conflicts locally:
  1. Pull the latest changes.
  2. Edit conflicting files manually.
  3. Stage and commit resolved files:
     ```sh
     git add <resolved-file>
     git commit -m "Resolve merge conflict in <file>"
     ```
- Ask for help if needed.

### Merging Pull Requests

- Once the PR is approved, merge it into `main` via GitHub.
- Only designated team members should merge PRs.

---

## 6. Pruning and Cleaning Up Branches

### Efficient Branch Cleanup After Merging

Once a feature branch is merged into `main`, update your local system and delete the branch:

```sh
git checkout main
git pull origin main
git branch -d feature/your-feature-name  # Delete local branch
git push origin --delete feature/your-feature-name  # Delete remote branch
git fetch --prune  # Clean up remote-tracking branches
```

### Automatically Prune Deleted Remote Branches

To remove all deleted remote branches from your local system:

```sh
git fetch --prune
```

To make this automatic every time you fetch or pull:

```sh
git config --global fetch.prune true
```

Now, Git will automatically clean up remote-tracking branches that no longer exist on GitHub.

---

## 7. Staying Updated Throughout the Hackathon

### Pull Regularly

Before starting any session and periodically during development:

```sh
git checkout main
git pull origin main
git checkout feature/your-feature-name  # If returning to your branch
```

### Updating Local Branches After Merging PRs

After merging a pull request on GitHub, update your local system:

```sh
git checkout main
git pull origin main
git fetch --prune  # Clean up remote-tracking branches
```

This keeps your local repository in sync and prevents conflicts.

---

## 8. Best Practices

✅ **Frequent Commits:** Commit changes regularly with clear messages.
✅ **Small PRs:** Keep pull requests focused and manageable.
✅ **Communicate:** Inform the team about progress and issues.
✅ **Use `.gitignore`:** Ensure sensitive files (e.g., `.env`) are ignored.
✅ **Clean Up Branches:** Delete merged branches to keep the repository tidy.
🚫 **Don't Force Push `main`:** Avoid force-pushing to `main` unless absolutely necessary.

---

## 9. Troubleshooting

### "Already up to date" when pulling:

- Ensure you're on the correct branch:
  ```sh
  git checkout main
  ```
- Verify the remote URL:
  ```sh
  git remote -v
  ```

### Handling Conflicts

- Take your time resolving them carefully.
- Ask for help if unsure!

---

**Happy hacking! 🚀**

