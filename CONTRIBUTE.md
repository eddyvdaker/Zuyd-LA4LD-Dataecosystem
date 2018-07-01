# How to contribute to LA4LD
So you are considering contributing to LA4LD, awesome! now what?

## Getting Support
To get help with the use of LA4LD, please use one of the following channels:
* [WIP]

Please do not use the Issue tracker for support requests.

## Reporting Issues
To make the issues as usefull as possible:
* Try to include a [minimal, complete, and verifiable examlpe](https://stackoverflow.com/help/mcve) to help reproduce and fix the issue.
* Describe what happend, including full traceback if available.
* List your Python and dependancy versions.

## Submitting Patches
* If your patch is code, include tests.
* Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) as much as possible.

### First Time Setup
* Download and install git
* Configure git with your email and username
```
git config --global user.name '{your username}'
git config --global user.email '{your email}'
``` 
* Create a [GitHub account](https://github.com/join)
* Fork LA4LD to your GitHub account by clicking the `Fork` button.
* Clone your GitHub fork locally
```
git clone https://github.com/{username}/Zuyd-LA4LD-Dataecosystem
cd Zuyd-LA4LD-Dataecosystem
```
* So you'll be able to update later, add the main repository as a remote
```
git remote add la4ld https://github.com/eddyvdaker/Zuyd-LA4LD-Dataecosystem
git fetch la4ld
```
* Create a Python virtual environmnent
```
python3 -m venv venv
. env/bin/activate
# or "env\Scripts\activate" on Windows
```

* Install LA4LD dependencies
```
pip install -r requirements.txt
```

### Developing the Patch
* Create a branch with the issue you would like to work on (for example `102-user-not-loading`)
* Make changes in the code
* Include tests to cover the changed code, make sure the tests fail without the changes
* Push your commits to GitHub
* Create a pull request on the main repository
* You're done!
