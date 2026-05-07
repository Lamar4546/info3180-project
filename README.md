======================================================================================================
DRIFTDATER
Dating Application
INFO3180 Group Project | 2025-2026
======================================================================================================

Repository : https://github.com/Lamar4546/info3180-project
Deployed   : https://info3180-project-wwkp.onrender.com/login


======================================================================================================
TABLE OF CONTENTS
======================================================================================================

  1. Project Description
  2. Team Members and Roles
  3. Technology Stack
  4. Setup Instructions
  5. Application Features
  6. API Documentation
  7. Database Design
  8. Deployment
  9. Known Issues and Limitations
  10. Submission Checklist


======================================================================================================
1. PROJECT DESCRIPTION
======================================================================================================

DriftDater is a full-stack web application built as part of the INFO3180 course.
It allows registered users to create detailed personal profiles, discover
compatible matches based on location, age range, and shared interests, and
communicate with users they have mutually liked. The application is built using
the Vue 3 frontend framework and a Flask REST API backend, with a PostgreSQL
database for persistent storage.

The platform implements the complete lifecycle of a dating application: account
creation and authentication, profile management with photo upload, a scored
matching algorithm, a like and pass system with mutual match detection, private
messaging restricted to matched users, full-text and filter-based search, and
the ability to save favourite profiles for later.


=====================================================================================================
2. TEAM MEMBERS AND ROLES
=====================================================================================================


  Name              Role                  Primary Responsibilities               GitHub
  ------------      --------------------  -------------------------------------  ---------
  Lamar Shaw        Project Manager       Timeline, coordination, documentation  @Lamar4546
  Oneil Marshall    Backend Lead          Flask API, database, authentication    @oneilmarshall2020
  Hosea Nichols     Frontend Lead         Vue 3 components, UI/UX, routing       @NixC0d3
  Nathan Hutton     Deployment Lead       Testing, validation, deployment        @Mxlten19

Note: Each member contributed to the codebase via their own GitHub branch.
All contributions are visible in the repository commit history.


======================================================================================================
3. TECHNOLOGY STACK
======================================================================================================

  Layer            Technologies
  ---------------  --------------------------------------------------------------
  Frontend         Vue 3, Vue Router 4, Pinia, Axios, Vite
  Backend          Python 3, Flask 3, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS
  Database         PostgreSQL (production), SQLite (local fallback)
  Authentication   Flask sessions, bcrypt password hashing via Werkzeug
  Deployment       Render (backend + PostgreSQL database)
  Version Control  Git, GitHub (feature branches per team member)


======================================================================================================
4. SETUP INSTRUCTIONS
======================================================================================================

The application has two parts that must be started separately: the Flask backend
API and the Vue frontend. Both must be running at the same time during
development.

--------------------------------------------------------------------------------
4.1 Prerequisites
--------------------------------------------------------------------------------

  - Python 3.10 or higher
  - Node.js 18 or higher and npm
  - PostgreSQL installed and running locally
  - Git

--------------------------------------------------------------------------------
4.2 Clone the Repository
--------------------------------------------------------------------------------

  git clone https://github.com/Lamar4546/info3180-project.git
  cd info3180-project

--------------------------------------------------------------------------------
4.3 Backend Setup
--------------------------------------------------------------------------------

Step 1: Create and activate a Python virtual environment.

  python -m venv venv
  source venv/bin/activate          # macOS / Linux
  .\venv\Scripts\activate           # Windows

Step 2: Install Python dependencies.

  pip install -r requirements.txt

Step 3: Create a PostgreSQL database.

  psql -U postgres
  CREATE DATABASE driftdater;
  \q

Step 4: Create a .env file in the project root with the following contents.
Replace the placeholder values with your own.

  SECRET_KEY=your-secret-key-here
  DATABASE_URL=postgresql://postgres:yourpassword@localhost/driftdater
  UPLOAD_FOLDER=app/static/uploads

Step 5: Run the database migrations to create all tables.

  flask --app app db upgrade

Step 6: Start the Flask development server.

  flask --app app --debug run

The backend API will be available at http://localhost:5000

--------------------------------------------------------------------------------
4.4 Frontend Setup
--------------------------------------------------------------------------------

Open a new terminal window in the project root directory.

Step 1: Install Node dependencies.

  npm install

Step 2: Start the Vite development server.

  npm run dev

The frontend will be available at http://localhost:5173

--------------------------------------------------------------------------------
4.5 Verifying the Setup
--------------------------------------------------------------------------------

With both servers running, open http://localhost:5173 in a browser. You should
see the DriftDater home page with options to register and log in. Register a
new account to confirm the database connection is working.


======================================================================================================
5. APPLICATION FEATURES
======================================================================================================

--------------------------------------------------------------------------------
5.1 Authentication and Profile Management
--------------------------------------------------------------------------------

  - User registration with email validation and unique username enforcement
  - Secure login and logout using Flask sessions
  - Passwords hashed with bcrypt via Werkzeug
  - Profile creation with the following fields:
      - First name, last name, date of birth, gender
      - Bio / personal description
      - Parish (location within Jamaica)
      - Preferred gender and age range for matching
      - Profile photo upload (PNG, JPG, GIF, WEBP, max 5 MB)
      - Interests and hobbies (minimum 3 required)
  - Profile visibility toggle (public or private)
  - Profile editing at any time after registration

--------------------------------------------------------------------------------
5.2 Matching System
--------------------------------------------------------------------------------

  - Scored matching algorithm that considers:
      - Shared interests (up to 50 points)
      - Age range compatibility (25 points)
      - Gender preference compatibility (25 points)
      - Same parish / location proximity (10 bonus points)
  - Browse mode showing profiles not yet acted on, sorted by match score
  - Like and Pass actions on individual profiles
  - Mutual match detection when both users like each other
  - Match notification displayed immediately when a mutual match occurs

--------------------------------------------------------------------------------
5.3 Messaging
--------------------------------------------------------------------------------

  - Messaging is restricted to mutually matched users only
  - Conversation list showing all active message threads
  - Unread message count displayed per conversation
  - Full message history with timestamps
  - Messages persisted to the database
  - Near-real-time message updates via 5-second polling

--------------------------------------------------------------------------------
5.4 Search and Discovery
--------------------------------------------------------------------------------

  - Search profiles by name or bio keyword
  - Filter by parish (location)
  - Filter by age range using sliders
  - Filter by interest keyword
  - Filter by gender
  - Results sorted by match score descending
  - Save profiles to a favourites list for later reference
  - Remove profiles from favourites at any time


======================================================================================================
6. API DOCUMENTATION
======================================================================================================

All endpoints are prefixed with /api. The backend runs on http://localhost:5000
in development. Endpoints marked as requiring authentication expect an active
session cookie, which is set automatically on login or registration.

--------------------------------------------------------------------------------
6.1 Authentication Endpoints
--------------------------------------------------------------------------------

  Method  Endpoint               Auth  Description
  ------  ---------------------  ----  -----------------------------------------
  POST    /api/auth/register     No    Register a new user account
  POST    /api/auth/login        No    Log in with email and password
  POST    /api/auth/logout       Yes   Terminate the current session
  GET     /api/auth/me           Yes   Return the currently logged-in user

POST /api/auth/register - Request Body:

  {
    "email":         "user@example.com",
    "username":      "johndoe",
    "password":      "minimum8chars",
    "first_name":    "John",
    "last_name":     "Doe",
    "date_of_birth": "1998-05-14",
    "gender":        "Male",
    "looking_for":   "Any",
    "parish":        "St. Catherine",
    "bio":           "Tell us about yourself...",
    "interests":     ["hiking", "music", "cooking"]
  }

--------------------------------------------------------------------------------
6.2 Profile Endpoints
--------------------------------------------------------------------------------

  Method  Endpoint                   Auth  Description
  ------  -------------------------  ----  -------------------------------------
  GET     /api/profiles/me           Yes   Return the current user's full profile
  PUT     /api/profiles/me           Yes   Update the current user's profile
  POST    /api/profiles/me/photo     Yes   Upload a profile photo (multipart)
  GET     /api/profiles/:id          No    View a profile by ID (public only)
  GET     /api/profiles              No    Search profiles with query parameters
  GET     /api/profiles/interests    No    List all registered interest tags

GET /api/profiles - Query Parameters:

  search    keyword matched against name and bio
  parish    exact match on parish name
  age_min   integer minimum age (default: 18)
  age_max   integer maximum age (default: 99)
  interest  exact match on a single interest name
  gender    exact match on gender field

--------------------------------------------------------------------------------
6.3 Matching Endpoints
--------------------------------------------------------------------------------

  Method  Endpoint               Auth  Description
  ------  ---------------------  ----  -----------------------------------------
  GET     /api/matches/browse    Yes   List unseen profiles with match scores
  POST    /api/matches/action    Yes   Submit a like or pass action
  GET     /api/matches           Yes   List all mutual matches

POST /api/matches/action - Request Body:

  { "profile_id": 7, "action": "like" }

  The action field accepts "like" or "pass". The response includes an is_match
  boolean indicating whether the action created a mutual match.

--------------------------------------------------------------------------------
6.4 Messaging Endpoints
--------------------------------------------------------------------------------

  Method  Endpoint                       Auth  Description
  ------  -----------------------------  ----  ---------------------------------
  POST    /api/messages/send             Yes   Send a message to a matched user
  GET     /api/messages/conversations    Yes   List conversations with last message
  GET     /api/messages/:partnerId       Yes   Retrieve full message history

POST /api/messages/send - Request Body:

  { "receiver_id": 3, "body": "Hey, how are you?" }

  Sending a message to a user who is not a mutual match returns a 403 error.

--------------------------------------------------------------------------------
6.5 Favourites Endpoints
--------------------------------------------------------------------------------

  Method  Endpoint               Auth  Description
  ------  ---------------------  ----  -----------------------------------------
  GET     /api/favorites         Yes   List all saved profiles
  POST    /api/favorites/:id     Yes   Add a profile to favourites
  DELETE  /api/favorites/:id     Yes   Remove a profile from favourites


======================================================================================================
7. DATABASE DESIGN
======================================================================================================

The database consists of five primary tables and two join tables, all in third
normal form. Flask-Migrate manages schema versioning through Alembic migration
scripts located in the migrations/versions/ directory.

--------------------------------------------------------------------------------
7.1 Tables
--------------------------------------------------------------------------------

  Table               Purpose
  ------------------  ----------------------------------------------------------
  users               Account credentials: email, username, hashed password
  profiles            Personal data: name, DOB, gender, bio, parish, photo,
                      preferences, and visibility setting
  interests           Normalised list of unique interest tag names
  likes               Records each like or pass action between two profiles,
                      with a unique constraint on liker_id + liked_id
  messages            Stores messages with sender, receiver, body, read status,
                      and timestamp
  profile_interests   Join table linking profiles to interests (many-to-many)
  profile_favorites   Join table for saved profiles (many-to-many, self-referential)

--------------------------------------------------------------------------------
7.2 Relationships
--------------------------------------------------------------------------------

  - users to profiles         : one-to-one (each user has exactly one profile)
  - profiles to interests     : many-to-many via profile_interests
  - profiles to likes         : one-to-many on both liker_id and liked_id
  - users to messages         : one-to-many on both sender_id and receiver_id
  - profiles to profiles      : many-to-many self-referential via profile_favorites

--------------------------------------------------------------------------------
7.3 Indexes
--------------------------------------------------------------------------------

  - users.email and users.username       unique indexes for fast login lookup
  - likes.liker_id and likes.liked_id    indexes for mutual match queries
  - messages.sender_id                   index for conversation queries
  - messages.receiver_id                 index for conversation queries
  - messages.created_at                  index for ordering message history

--------------------------------------------------------------------------------
7.4 Running Migrations
--------------------------------------------------------------------------------

To apply all migrations on a fresh database:

  flask --app app db upgrade

To create a new migration after modifying models.py:

  flask --app app db migrate -m "describe the change"
  flask --app app db upgrade


======================================================================================================
8. DEPLOYMENT
======================================================================================================

The application is deployed to Render. The backend runs as a web service and
connects to a Render-managed PostgreSQL database. The deployed URL is listed
at the top of this document.

Environment variables required on Render:

  SECRET_KEY      A long random string. Never use the development default.
                  Generate one with:
                  python -c "import secrets; print(secrets.token_hex(32))"

  DATABASE_URL    Provided automatically by Render when a PostgreSQL service
                  is linked to the web service.

  UPLOAD_FOLDER   Set to a writable path, or configure an external storage
                  service such as AWS S3 or Cloudinary for persistent uploads.

Build command:

  pip install -r requirements.txt && flask --app app db upgrade

Start command:

  gunicorn main:app


======================================================================================================
9. KNOWN ISSUES AND LIMITATIONS
======================================================================================================

  - Profile photo uploads are stored on the local filesystem. On Render's free
    tier the filesystem is ephemeral, meaning uploaded photos are lost on each
    redeploy. For production use, photos should be stored in an external service
    such as AWS S3 or Cloudinary.

  - The messaging system uses 5-second polling rather than WebSockets. There is
    a small delay between a message being sent and it appearing on the
    recipient's screen without a manual refresh.

  - Password reset functionality is not implemented in this version.

  - There is no email verification step after registration.

  - The matching algorithm is rule-based scoring and does not use machine
    learning or collaborative filtering.


======================================================================================================
10. SUBMISSION CHECKLIST
======================================================================================================

  [ ] All source code pushed to GitHub
  [ ] README is complete and accurate
  [ ] Database migrations run without errors on a fresh install
  [ ] No sensitive data committed to the repository (.env is in .gitignore)
  [ ] requirements.txt and package.json are up to date
  [ ] Application runs without errors from a clean clone
  [ ] Git history shows commits from all team members
  [ ] Deployed application URL is working and listed at the top of this file
  [ ] Presentation slides prepared


======================================================================================================
CONTACT
======================================================================================================

Course Coordinator : Mr. Laurie Ivor Leitch
Email              : laurie.leitch@uwi.edu
Office             : UWI, Mona MITS

======================================================================================================