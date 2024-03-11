## Testing builds locally

GitHub Actions provides a convinient way to automate the build process 
(running tests, linter, compatibilty on various Python versions etc.).
It can be triggred using "events" such as creating a PR or pushing changes
to a specific branch. We specify yaml files in the workflows directory 
(default location where GitHub looks for configs), to specify the build process in detail.

However, it can be tricky to configure them correctly so it's good to 
test it locally before pushing changes. This is important for two reasons:

- Limited usage hours on workflows for free accounts [link](https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration)

- Iterating locally is typically much faster than pushing changes each time we want to test the config file.

Step 1: When running this for the first time, pull the docker Ubuntu Python3.9 image,

```bash
docker pull python:3.9-slim-bullseye
```

Step 2: Initialize the build using the Dockerfile

```bash 
docker build -t impact-challenge -f .github/Dockerfile .
```

Step 3 (optional): Run it interactively, to test it.

```bash
docker run -it impact-challenge
```