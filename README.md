# Flask Blog Application

This is a blog application built with Flask, featuring user registration, login, account management, and post creation functionalities. It uses blueprints to modularize code and SQLAlchemy with SQLite for database management. Additionally, password hashing with bcrypt and image uploads are implemented, as well as email support for password reset.

## Features

- **User Authentication**: Register, login, logout, and profile update.
- **Blog Post Management**: Create, update, and delete posts.
- **Account Management**: Update user information and profile picture uploads.
- **Password Reset**: Request password reset via email link.
- **Image Uploads**: Upload profile pictures with size optimization.
- **Blueprints**: Modularized code structure.
- **Database**: SQLite with SQLAlchemy ORM.
- **Flask-Mail**: For sending password reset emails.

## Requirements

- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Mail
- Flask-Login
- Pillow (for image processing)
- Flask-WTF

Install requirements with:

```bash
pip install -r requirements.txt
```

## Application Structure

The application uses **blueprints** to organize routes for different sections:

- **`users`** blueprint for user registration, login, logout, and profile management.
- **`posts`** blueprint for managing blog posts.
- **`main`** blueprint for static pages, such as the home and about pages.

### Key Files and Directories

- `app.py`: Main application entry point.
- `flaskblog/`: Contains application modules and blueprints.
  - `users/`: User-related functionalities like registration and login.
  - `posts/`: Blog post creation and management.
  - `main/`: Static pages like the home and about pages.
- `static/profile_pics`: Stores uploaded profile pictures.
- `templates/`: HTML templates for rendering web pages.

## Configuration

1. **Database**: The application uses SQLite as the default database. The database models are defined using SQLAlchemy in `flaskblog/models.py`.
2. **Image Uploads**: Profile pictures are stored in `static/profile_pics`. The `savePicture` function in `flaskblog/users/utils.py` handles image resizing and saving.
3. **Email Configuration**: Configure `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, and `MAIL_PASSWORD` in your environment or Flask config for password reset emails.

## Routes

### User Routes (`users` Blueprint)

- **`/register`**: Register a new user.
- **`/login`**: User login.
- **`/logout`**: Logout the current user.
- **`/account`**: Manage user account details.
- **`/user/<username>`**: View posts by a specific user.
- **`/resetPassword`**: Request a password reset link via email.
- **`/resetPassword/<token>`**: Reset password using the link sent in email.

### Blog Post Routes (`posts` Blueprint)

- **`/post/new`**: Create a new blog post.
- **`/post/<post_id>`**: View a specific post.
- **`/post/<post_id>/update`**: Update a post.
- **`/post/<post_id>/delete`**: Delete a post.

### Static Routes (`main` Blueprint)

- **`/home`**: Home page displaying recent posts.
- **`/about`**: Static about page.

## Running the Application

1. **Initialize the Database**:

   ```bash
   python3
   ```

- This will open the python interpreter the execute following to create a database
  ```python
  from flaskblog import db, app
  create_db = lambda: (app.app_context().push(), db.create_all())
  create_db()
  ```

2. **Run the Flask Server**:

   ```bash
   python3 run.py
   ```

3. **Access the App**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## Example Usage

1. **Register and Login**: Create a user account and log in.
2. **Create a Post**: Write and publish a new blog post.
3. **Manage Account**: Update profile details or request a password reset if needed.

## Additional Notes

- **Profile Picture Management**: Upload a profile picture on the account page, where it is resized and stored in the `profile_pics` folder.
- **Password Reset**: Use the reset password functionality to receive a reset link in your email.

## Contributing

If you have suggestions for improving this load balancer, please feel free to contribute by opening a pull request.
