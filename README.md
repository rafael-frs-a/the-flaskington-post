# About

This is my first GitHub repository. Its idea is to be a simple blog application made in Python using the Flask framework. My main purpose here was to learn the language and framework by developing a web application with practical (although not original) use.

# Blog Features

Since it's meant to be a blog, the main feature of this web application is writing posts in a rich text editor, contemplating the basic CRUD operations. In addition, the app also counts with the following features:

- Account features:
  - Sign up;
  - Account confirmation via email;
  - Login/logout;
  - Password recovery;
  - Upload profile picture;
  - Delete account;
- Security:
  - Password hashing;
  - HTML sanitization;
- Admin features:
  - CRUD operations on users;
  - Ban user;
  - CRUD operations on users' roles;
  - View and delete posts;
  - CRUD operations on emails.

# Dependencies

This project was made mainly in Python, specifically version 3.6.8. The packages used for the development of its features are listed in the *requirements.txt* file located at the root of the project.

# Configuration

## Environment Variables

If you want to run this project, you'll need to set some environment variables first. The **FLASK_APP** variable should be set to *tfp/app.py*. Besides that, there is also:

- **DATABASE_URL**: your database location, used by SQLAlchemy object;
- **SECRET_KEY**: used by some of the Python packages, such as SQLAlchemy and WTForms;
- **MAIL_USERNAME**: the email address that will be used to send emails to the registered users;
- **MAIL_PASSWORD**: the password of the previous email account;
- **MAIL_SERVER**: the previous email account server. E.g.: smtp.gmail.com;
- **MAIL_PORT**: the email account port;
- **MAIL_USE_SSL**: boolean flag to define if the connection to the email account uses SSL or not.

To make it easier, you can create a *.env* file at the root of the project informing the previous environment variables. Since the app uses python-dotenv, the variables defined in this file will be exported when the command *flask run* is executed. You can also create a separate *.flaskenv* file in the same location to define other development variables like **FLASK_APP** or **FLASK_ENV**.

## Custom Commands

The project contains three client commands that can be executed on the terminal:

- **flask create-db**: command to create the database and all the tables defined in the models;
- **flask drop-db**: command to drop all the tables of the database;
- **flask create-admin**: command to create a default admin user, with username *admin* and password *admin*.
