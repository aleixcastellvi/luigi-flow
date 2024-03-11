## Description

***Under construction...***

## Setting Up the Repository with GitHub
 
1. Create a Repository on GitHub

* Access your GitHub account.
* Click the "New" button to create a new repository.
* Fill in the required information and click "Create repository."

2. Initialize the Local Repository

This step is essential at the project's outset to manage version control.

```bash
git init
git add .
git commit -m "First commit"
```

3. Linking to the GitHub Remote Repository

Link the local source code repository with the GitHub environment.

```bash
git remote add origin https://github.com/username/repository-name.git
```

*Make sure to replace "username" and "repository-name" with your GitHub username and your repository's name, respectively.*

These steps establish the connection between your local repository and the GitHub repository, allowing you to track changes and collaborate effectively.

## Setting up a Virtual Environment

**Conda (Mac OSX)**

```bash
conda create -n pyspark-flow python=3.10

conda activate pyspark-flow
```

Install dependencies with pip

```bash
pip install -r requirements.txt
```

Run the app

```bash
python app.py
```