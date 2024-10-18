# Videoflix

Videoflix is a web application that allows users to upload, manage, and save their favorite videos. This application is developed using Django as the backend and Angular as the frontend.

## Features

-   User registration and login
-   Video upload and management
-   Creation of thumbnails and screenshots
-   Video conversion to various resolutions
-   Favorites feature for users
-   API endpoints for interaction with the frontend application

## Technologies

-   **Backend**: Django, Django REST Framework
-   **Frontend**: Angular
-   **Database**: PostgreSQL
-   **Caching**: Redis layer caching,, Django RQ
-   **Video Processing**: FFmpeg

## Installation

### Backend

1. Clone the repository:
   git clone https://github.com/christian-grund/videoflix-backend
   cd videoflix-backend

2. Create and activate a virtual Python environment:
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install the dependencies:
   pip install -r requirements.txt

4. Configure the database in settings.py and run the migrations:
   python manage.py migrate

5. Start the server:
   python manage.py runserver

### Frontend

1. Clone the repository:
   git clone https://github.com/christian-grund/videoflix-frontend
   cd videoflix-frontend

2. Install the dependencies:
   npm install

3. Start the application:
   ng serve

## Usage

-   Visit http://localhost:4200 for the frontend application.
-   Use the API endpoints for backend interactions.

## Testing

To run the tests, navigate to the backend folder and execute the following command:
python manage.py test
