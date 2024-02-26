# Library Django Application

## Description

The Library Django application allows users to register, recover passwords, change passwords, and update their profile picture. Users can leave comments on books, borrow books from the library, change the return date, view information on borrowed books, and return books (CRUD functionality). Additionally, users can browse all books, authors, and get detailed information about books or authors. This functionality is available for both registered and unregistered users.

## Usage

### Admin Page
Access the admin page [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) with the following credentials:
- Username: admin
- Password: adminadmin123

On the admin page, you can create and manage records for books, authors, book copies, genres, reviews, and users.

### User Features
- Register an account
- Recover password
- Change password
- Update profile picture
- Leave comments on books
- Borrow books from the library
- Change return dates
- View information on borrowed books
- Return books

### Public Features
- Browse all books
- View details about authors
- View details about books
- View book or author information

## Installation

1. Clone the project using the `git clone` command:

    ```bash
    git clone https://github.com/LUNOTHEDOG/BIBLIOTEKA.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Django server:

    ```bash
    python manage.py runserver
    ```

4. Open a web browser and go to [http://localhost:8000/](http://localhost:8000/) to access the application.

## Contact
 varngie@gmail.com
