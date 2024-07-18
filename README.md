Updates to keyboard shortcuts … On Thursday 1 August 2024, Drive keyboard shortcuts will be updated to give you first-letter navigation.Learn more
---
# T-Plot

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![Githun Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white) ![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
[![CICD](https://github.com/L7G9/tplot/actions/workflows/main.yaml/badge.svg)](https://github.com/L7G9/tplot/actions/workflows/main.yaml) [![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Timeline web app

---
T-Plot is a web app which can be used to create timelines as a list of events, these are used to create a perfectly scaled PDF of the timeline.
The user sets the scale and layout settings they want, and the app automatically handles the correct positioning of the events on PDF.
Created to demonstrate the use of the web framework Django, it features a fully functional CI/CD pipeline that deploys it on AWS Elastic Beanstalk.

The current release up and running [here](https://tplot.lukegregorydev.co.uk).

---
## Implemented Features
  - User registration, login and logout
  - Create, read, update and delete timeline information in a Postgres database running on AWS RDS
  - Permissions to ensure users can only view their own database records
  - Timeline Types
    - Date and Time using events ordered by calendar and clock time units including years, months, weeks, days, hours, minutes and seconds
    - Age using events ordered by age in years and months
  - Timeline Views
    - Web based timeline
    - PDF timeline
      - Set timeline scale
      - Control PDF layout
  - User Guide
    - Getting started guides for common tasks
    - Reference guides explaining all TPlot's objects, values and settings
  - AI Assist
    - Request ChatGPT find potential events you add to your timeline
    - Review the results and select which events to add
  - High availability using AWS EC2 instances in an Auto Scaling Group with a Load Balancer

## Project Road Map
  - Timeline Types
    - Years BC to AD
    - Thousands/Millions/Billions of years in the past and future
  - Ways to view timelines
    - Web based representation
    - Slide show
  - Use AWS S3 to allow users to store images with their timelines
  - Sharing and collaboration
  - Register with Google, GitHub etc

---
## CI/CD

This project uses 3 workflows which showcase some of the possibilities if GitHub Actions.
  - Manually triggered workflow to create or terminate the Elastic Beanstalk production environment.
    - [Elastic Beanstalk Environment](https://github.com/L7G9/tplot/blob/main/.github/workflows/ebs_environment.yaml)
  - Reusable workflow to test if the production environment is up and running.
    - [Elastic Beanstalk Environment Status](https://github.com/L7G9/tplot/blob/main/.github/workflows/ebs_environment_status.yaml)
  - Continuous Integration / Continuous Deployment pipeline that tests the code before integrating it with the main branch.  Then it will deploy to the production environment if it is running.
    - [CI/CD](https://github.com/L7G9/tplot/blob/main/.github/workflows/main.yaml)
  - Automated setup and terminate of access through AWS Route53 and HTTPS using Boto3.
    - [Setup Https](https://github.com/L7G9/tplot/tree/main/python_scripts/awseb_https)
    - [Delete Route53 Alias Record](https://github.com/L7G9/tplot/tree/main/python_scripts/delete_alias)
    - [Delete ACM Certificate](https://github.com/L7G9/tplot/tree/main/python_scripts/delete_certificate)

---
## Author

[@L7G9](https://www.github.com/L7G9)

---
## Acknowledgements

All these resources were used to create this project.  Thank you to all those who took the time and effort to share.
- [Django](https://www.djangoproject.com/)
- [Django User Login](https://ordinarycoders.com/blog/article/django-user-register-login-logout)
- [Django Postgres Setup](https://blog.nextideatech.com/how-to-create-a-django-app-and-connect-it-to-a-database/)
- [Crispy Bootstrap 4](https://pypi.org/project/crispy-bootstrap4/)
- [Elastic Beanstalk Deploy Action](https://github.com/einaregilsson/beanstalk-deploy)
- [Elastic Beanstalk CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Django Deployment on EBS](https://testdriven.io/blog/django-elastic-beanstalk/)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)
- [Coverage](https://coverage.readthedocs.io/en/7.3.1/)
- [Black](https://pypi.org/project/black/)
- [Flake8](https://pypi.org/project/flake8/)
- [Bandit](https://pypi.org/project/bandit/)

---
