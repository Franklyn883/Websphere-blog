# WebSphere
WebSphere is a dynamic blogging platform where users can write, edit, and delete blog posts. Users can also engage with content through comments, replies, likes, and bookmarks. The project leverages modern web technologies to provide a smooth and responsive user experience.

## Features

- **User Authentication**: Secure user authentication with Django Allauth, including email validation and social signups.
- **Blog Posts**: Users can create, edit, and delete blog posts.
- **Comments**: Users can add, edit, and delete comments on blog posts.
- **Replies**: Users can reply to comments, as well as edit and delete their replies.
- **Likes**: Users can like blog posts, comments, and replies.
- **Bookmarks**: Users can bookmark their favorite blog posts for easy access.
- **Smooth UX**: Enhanced user experience with HTMX for seamless content updates without full page reloads.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **User Experience**: HTMX
- **Authentication**: Django Allauth

## Installation

To get a local copy up and running, follow these simple steps:

### Prerequisites

- Python 3.7+
- Django 3.2+
- Virtualenv (optional, but recommended)

#### Clone the Repository

- `git clone https://github.com/Franklyn883/Websphere-blog.git`
- `cd websphere`

#### Create and Activate a Virtual Environment
- `python -m venv venv`
- source venv/bin/activate  # On Windows use `venv\Scripts\activate`

#### Install Dependencies
- `pip install -r requirements.txt`

#### Apply Migrations
- `python manage.py migrate`

### Create a Superuser
`python manage.py createsuperuser`

#### Run the Server
- `python manage.py runserver`

## Usage
### Writing a Blog Post
- Register or log in to your account.
- Navigate to the "New Post" section.
- Fill in the title,subtitle, select the category, and content for your blog post.
- Click "Publish" to share your post with the community.
Interacting with Posts

#### Commenting: 
- Add comments to engage with the content. 
- Edit or delete your comments as needed.
#### Replying: 
- Reply to comments and manage your replies.
#### Liking: 
- Show your appreciation by liking posts, comments, and replies.
#### Bookmarking: 
- Bookmark your favorite posts for easy access later.

## Contributing
Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

- Fork the Project
- Create your Feature Branch (git checkout -b feature/AmazingFeature)
- Commit your Changes (git commit -m 'Add some AmazingFeature')
- Push to the Branch (git push origin feature/AmazingFeature)
- Open a Pull Request


## Contact
Email: Frankalimimian@gmail.com




