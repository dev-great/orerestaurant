<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">ORE RESTAURANT-README-SETUP</h3>

  <p align="center">
    An awesome README to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://orerestaurant.pythonanywhere.com/api/v1/docs">View Demo</a>
    ·
    <a href="https://github.com/dev-great/orerestaurant/issues">Report Bug</a>
    ·
    <a href="https://github.com/dev-great/orerestaurant/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Ore is an restaurant owner where people can order from her store, make enquiries, and also, importantly, where her staff can add, remove, and update the menu.

Use the `BLANK_README.md` to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![python][python]][python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Make sure you have **Python 3.x**  or **Python 4.x** installed and **the latest version of pip** *installed* before running these steps.

Clone the repository using the following command

```bash
git clone git@github.com:dev-great/orerestaurant.git
# After cloning, move into the directory having the project files using the change directory command
cd orerestaurant_db
```
Create a virtual environment where all the required python packages will be installed

```bash
# Use this on Windows
python -m venv env
# Use this on Linux and Mac
python -m venv env
```
Activate the virtual environment

```bash
# Windows
.\env\Scripts\activate
# Linux and Mac
source ./env/bin/activate
```

## Install and Run

Install all the project Requirements
```bash
pip install -r requirements.txt
```
-Apply migrations and create your superuser (follow the prompts)

```bash
# apply migrations and create your database
python manage.py migrate

# Create a user with manage.py
python manage.py createsuperuser
```

Create .env file 

```bash
# create your .env file and add the follow to it; SECRET_KEY, EMAIL_USER, EMAIL_PASSWORD, ENVIRONMENT, CLOUD_NAME, API_KEY, API_SECRET 
```

Run the tests

```bash
# run django tests for pytest 
pytest
```

```bash
# run django tests 
python manage.py test 
```

Run the development server

```bash
# run django development server
python manage.py runserver
```
## Reviewers 

After submitting your PR, please tag reviewer(s) in your PR message. You can tag anyone below for the following.

<br/>

- **Markdown, Documentation, Email templates:**

  [@dev-great](https://github.com/dev-great)

#


## Explore admin panel for model data or instances

http://127.0.0.1:8000/admin or http://localhost:8000/admin

## Login with the user credentials (you created) using "createsuperuser" cmd

> ⚠ If everything is good and has been done successfully, your **Django Rest API** should be hosted on port 8000 i.e http://127.0.0.1:8000/ or http://localhost:8000/



<!-- CONTRIBUTING -->
## Contributing

1. Clone the Project developmet branch
2. Create your Feature Branch (`git checkout -b branchname`)
2. Track updated files (`git status`)
2. init untraced files (`git add paste_copied_untracked_file`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the  Apache License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Waitlist Site - [https://www.orerestaurant.com](https://www.orerestaurant.com) 

Project Link: [https://github.com/dev-great/orerestaurant](https://github.com/dev-great/orerestaurant)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=yellow
[python-url]: https://python.com

[Discord]: https://discord.gg/bS7446M4
[product-screenshot]: project_sample.png
[codeOfConduct]: https://github.com/dev-great/orerestaurant/blob/main/LICENSE

[discordBadge]: https://img.shields.io/discord/842728941088931870?color=7289da&label=discord&logo=discord&logoColor=white
[CodeOfConductBadge]: https://img.shields.io/badge/Code%20of%20Conduct-Contributor%20Covenant%202.0-4baaaa.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiBmaWxsPSJ3aGl0ZSI+PHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNOC41MzMuMTMzYTEuNzUgMS43NSAwIDAwLTEuMDY2IDBsLTUuMjUgMS42OEExLjc1IDEuNzUgMCAwMDEgMy40OFY3YzAgMS41NjYuMzIgMy4xODIgMS4zMDMgNC42ODIuOTgzIDEuNDk4IDIuNTg1IDIuODEzIDUuMDMyIDMuODU1YTEuNyAxLjcgMCAwMDEuMzMgMGMyLjQ0Ny0xLjA0MiA0LjA0OS0yLjM1NyA1LjAzMi0zLjg1NUMxNC42OCAxMC4xODIgMTUgOC41NjYgMTUgN1YzLjQ4YTEuNzUgMS43NSAwIDAwLTEuMjE3LTEuNjY3TDguNTMzLjEzM3ptLS42MSAxLjQyOWEuMjUuMjUgMCAwMS4xNTMgMGw1LjI1IDEuNjhhLjI1LjI1IDAgMDEuMTc0LjIzOFY3YzAgMS4zNTgtLjI3NSAyLjY2Ni0xLjA1NyAzLjg2LS43ODQgMS4xOTQtMi4xMjEgMi4zNC00LjM2NiAzLjI5N2EuMi4yIDAgMDEtLjE1NCAwYy0yLjI0NS0uOTU2LTMuNTgyLTIuMTA0LTQuMzY2LTMuMjk4QzIuNzc1IDkuNjY2IDIuNSA4LjM2IDIuNSA3VjMuNDhhLjI1LjI1IDAgMDEuMTc0LS4yMzdsNS4yNS0xLjY4ek0xMS4yOCA2LjI4YS43NS43NSAwIDAwLTEuMDYtMS4wNkw3LjI1IDguMTlsLS45Ny0uOTdhLjc1Ljc1IDAgMTAtMS4wNiAxLjA2bDEuNSAxLjVhLjc1Ljc1IDAgMDAxLjA2IDBsMy41LTMuNXoiPjwvcGF0aD48L3N2Zz4=

[sizeBadge]: https://img.shields.io/github/repo-size/dev-great/recent-activity?
