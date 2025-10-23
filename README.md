# Demo

This repository demonstrates integration with Codecov.

## Setup Instructions

1. **Fork the Repository**
    - Click the **"Fork"** button at the top right of this repository on GitHub.
    - This will create a copy of the repository under your own GitHub account.

2. **Clone your forked repository:**
```bash
git clone https://github.com/your-username/codecov-demo-repo.git
cd codecov-demo-repo
```

3. **Add a Codecov Token:**
   - In your GitHub repository, navigate to **Settings** > **Secrets and variables** > **Actions**.
   - Click **New repository secret** and add your Codecov token with the name `CODECOV_TOKEN`.

2. **Install Dependencies:**
   - Run `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt` to install the necessary Python packages.

4. **Run Tests:**
   - Execute `PYTHONPATH=$(pwd) pytest --cov=src --cov-report=xml` to run tests and generate a coverage report. Run `--junitxml=junit.xml -o junit_family=legacy` to the command to generate a JUnit report. 

5. **Continuous Integration:**
   - The repository is set up with GitHub Actions to run tests and upload coverage reports to Codecov on each push and pull request.

------

*For the owner of the demo repository, since you can't fork:*

1. **Add a Codecov Token:**
   - In your GitHub repository, navigate to **Settings** > **Secrets and variables** > **Actions**.
   - Click **New repository secret** and add your Codecov token with the name `CODECOV_TOKEN`.

2. **Creating a Test Repository Based on This Template:**
    - Create a new repository in github (e.g., codecov-test-repo)
    ```
    git clone --bare https://github.com/Kobby-Bawuah/codecov-demo-repo.git
    cd codecov-demo-repo.git
    git push --mirror https://github.com/your-username/codecov-test-repo.git
    cd ..
    rm -rf codecov-demo-repo.git
    ```
3. **Clone the new repository:**
    ```
    git clone https://github.com/your-username/codecov-test-repo.git
    cd codecov-test-repo
    ```

3. **Install Dependencies:**
   - Run `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt` to install the necessary Python packages.

4. **Run Tests:**
   - Execute `PYTHONPATH=$(pwd) pytest --cov=src --cov-report=xml` to run tests and generate a coverage report. Run `--junitxml=junit.xml -o junit_family=legacy` to the command to generate a JUnit report. 

5. **Continuous Integration:**
   - The repository is set up with GitHub Actions to run tests and upload coverage reports to Codecov on each push and pull request.


hiii
