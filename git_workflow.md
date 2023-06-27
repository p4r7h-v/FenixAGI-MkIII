## Git Workflow for Working on a New Feature

When working on a new feature in your Python project, it's important to use Git properly to manage your changes. Here's a step-by-step guide on how to use Git with an example of working on the `fenix.py` file.

1. **Clone the repository**: Start by cloning the repository to your local machine using the command:
   ```
   git clone <repository_url>
   ```

2. **Create a new branch**: Create a new branch for your feature using a descriptive name. For example:
   ```
   git checkout -b feature/new-feature
   ```

3. **Make changes**: Make your desired changes in the `fenix.py` file using your preferred text editor or IDE.

4. **Stage changes**: Use the following command to stage your changes:
   ```
   git add fenix.py
   ```

5. **Commit changes**: Commit your changes with a meaningful commit message:
   ```
   git commit -m 'Implemented new feature'
   ```

6. **Push changes**: Push your branch to the remote repository:
   ```
   git push origin feature/new-feature
   ```

7. **Create a pull request**: Go to the repository's web interface and create a pull request for your changes. Provide a clear description of your feature and submit the pull request.

8. **Review and incorporate feedback**: Collaborate with your teammates and address any feedback or comments on your pull request.

9. **Merge the pull request**: Once your changes have been reviewed and approved, merge your pull request into the main branch of the repository.

10. **Cleanup**: After merging, you can delete the branch using the command:
    ```
    git branch -d feature/new-feature
    ```

Remember to regularly pull the latest changes from the main branch to keep your local repository up to date.
