## Description

This Luigi application retrieves data from the [CoinMarketCap API](https://coinmarketcap.com/api/pricing/) related to cryptocurrencies. The data is processed to obtain the top 100 coins sorted by market value, and a CSV file is generated. The generated file is saved in the directory specified in the ***config*** file.

If the file has already been generated, the Luigi task detects it and does not rerun the process, ensuring efficiency and preventing unnecessary API calls. The API calls are made in accordance with the guidelines outlined in the documentation provided by `CoinMarketCap`.

## Setting up a Virtual Environment

**Conda (macOS)**

```bash
conda create -n luigi-flow python=3.10

conda activate pyspark-flow
```

Install dependencies with pip

```bash
pip install -r requirements.txt
```

--- 

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

Link the local repository to the GitHub remote repository by running the following command:

```bash
git remote add origin https://github.com/username/repository-name.git
```

After creating the remote branch named `origin` that links the local repository, it's essential to assign a name to the current branch, which will become the main branch in our repository. Our main branch will be named **main**:

```
git branch -M main
```

Use the following command to push local changes to the main branch. The `-u` option indicates that the main branch will be the default for the remote `origin`. In the future, a *push* or *pull* will default to the **main** branch of origin.

```
git push -u origin main
```

*Make sure to replace "username" and "repository-name" with your GitHub username and your repository's name, respectively.*

These steps establish the connection between your local repository and the GitHub repository, allowing you to track changes and collaborate effectively.