[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE.txt)

Django Docker Boilerplate - Django Rest Framework
===============================================================================

## Note
- The template is using foundation as a framework but this can be changed by your personal preference, you only need to update the references in the `static` and `templates` folder.
- Comes with a bunch of plugins for many kinds of projects. Not all of them are needed, feel free to remove what yuo don't need
- This boilerplate is now supporting [Django Channels](https://channels.readthedocs.io/en/stable/index.html).
- Read more about this [here](https://channels.readthedocs.io/en/stable/index.html)

# To install from template base
- `django-admin startproject --template=https://github.com/tiagoarasilva/django-boilerplate/archive/master.zip --extension=py,md,html,txt,scss,sass project_name`
- Make sure you change the project name
- The tests for the views won't work until you implement the solution to make the tests passing! TDD oriented.

# Docker
- Change the {{ project_name }} in your docker file to the desired name

# {{ project_name }} Docker
-  Run `docker volume create --name={{ project_name }}_db_data`
-  Run `docker-compose up`. It will download all the resources needed to build your docker image
-  Run `docker-compose exec {{ project_name }} bash` to go inside the container
-  Run `make run` to start the server (inside docker container)
-  Run `make shell` to start the shell_plus

If you want, you can create alias in your local machine inside the bash_profile to do automatically this for you

E.g.:

```Shell
alias shell_plus='docker-compose up exec {{ project_name }} bash && make run'
alias run_server='docker-compose up exec {{ project_name }} bash && make shell'
```

# First run with the project
- Inside docker container:
    - Run `make migrate´. This is a special command inside the Makefile to run the first migrations or if you are on windows or you don't want to run the Makefile, just type `python {{ project_name }} migrate`
    - Run `python {{ project_name }} createsuperuser` to create a super user for yourself
    - It will create a "User Admin" by default as first and last name respectively. This can be changed in `accounts/management/commands/createsuperuser.py`


# Run Tests (If you ran migrations before and need to reconstruct the DB schema)
`make unittests TESTONLY='profiles.tests.models_tests'`
- OR
`make unittests TESTONLY='profiles.tests.models_tests:ProfileUserTest.test_create_user'` for a specific test

# If you only need to run the tests and models weren't changed before
`make reusedb_unittests TESTONLY='profiles.tests.models_tests`
### apps

All of your Django "apps" go in this directory. These have models, views, forms,
templates or all of the above. These should be Python packages you would add to
your project's `INSTALLED_APPS` list.


### Requirements for MacOS and Windows

Install Homebrew (MacOS Users)
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

Install OpenSSL or Upgrade (MacOS Users)
`brew install openssl`

### Requirements for Linux (Ubuntu >= 16.10)
Install OpenSSL or Upgrade
`sudo apt update`
`sudo apt install openssl-server`

### Requirements for Linux (Ubuntu <= 16.10)
Install OpenSSL or Upgrade
`sudo apt-get update`
`sudo apt-get install openssl-server`


Install VirtualenvWrapper
`https://virtualenvwrapper.readthedocs.io/en/latest/install.html`

Upgrade pip
`pip install --upgrade pip`

### Templates

Project-wide templates are located in templates/

#### manage.py

The standard Django `manage.py`.

#### settings.py

Many good default settings for Django applications

#### urls.py

{{ project_name }}`url_patterns` to serve static media when in solo development mode.
