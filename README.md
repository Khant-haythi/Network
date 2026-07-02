# Network
## 📖 Overview
Network is a Twitter-like social network website built as Project 4 for Harvard's CS50W (Web Programming with Python and JavaScript). Users can make posts, follow other users, and "like" or "unlike" posts. 

**🎥 Watch the Video Demo:** [YouTube Link](https://youtu.be/Ph2laQRd814?si=ka0Cg9MrZlID3yA3)

## ✨ Features
This project implements the following features, as demonstrated in the video demo:

*   **New Post (0:03):** Logged-in users can write and submit a new text-based post.
*   **All Posts (0:19):** A feed displaying all posts from all users, showing the username, content, timestamp, and like count.
*   **Profile Page (0:28):** Clicking on a username loads their profile, showing their followers, who they are following, and all of their previous posts. 
*   **Following (0:59):** Users can follow or unfollow other profiles. A dedicated "Following" page displays posts exclusively from the users they follow.
*   **Pagination (1:12):** Posts are paginated, displaying 10 posts per page with "Next" and "Previous" navigation buttons.
*   **Edit Post (1:29):** Users can securely edit their own posts via JavaScript without reloading the entire page.
*   **Likes and Unlike (1:41):** Users can asynchronously toggle a "like" on any post, dynamically updating the like count without a page reload.

## 🛠️ Tech Stack
*   **Backend:** Python, Django
*   **Frontend:** JavaScript, HTML, CSS
*   **Database:** SQLite (Default Django DB)

## 🚀 How to Run the Project
1. Clone this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Install the required dependencies (if you have a `requirements.txt`):
   ```bash
   pip install -r requirements.txt

4. Make and apply database migrations:
```bash
   python manage.py makemigrations
   python manage.py migrate

5. Run the development server:
```bash
   python manage.py runserver

6. Open a web browser and navigate to http://127.0.0.1:8000/.
