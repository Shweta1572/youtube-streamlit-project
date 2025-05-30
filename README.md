# YouTube Channel Analyzer

This is a full-stack, containerized web application built with **Streamlit**, **MongoDB**, and **Mongo Express**, orchestrated using **Docker Compose**.

The app allows users to:

* Fetch and display YouTube Channel information.
* Fetch a list of all videos from a YouTube channel.
* Save the fetched data into a MongoDB database.
* Manage and view the database using Mongo Express Admin UI.

---

##  How to Run This Project

### 1. Clone this repository


git clone git@github.com:Shweta1572/youtube-streamlit-project.git
cd youtube-streamlit-project


### 2. Requirements

* **Docker** installed ([Get Docker](https://docs.docker.com/get-docker/))
* **Docker Compose** installed (comes with Docker Desktop)
* **YouTube API Key** ([How to get API Key](https://console.cloud.google.com/apis/credentials))

### 3. Start the App

docker-compose up --build

This will start:

* Streamlit app on [http://localhost:8501](http://localhost:8501)
* Mongo Express Admin UI on [http://localhost:8081](http://localhost:8081)

###  Using the App

* Enter your **YouTube API Key** and **Channel ID** in the Streamlit app.
* Click **Get Channel Info** to fetch and store channel details.
* Click **Get All Videos** to fetch and store videos list.
* Open Mongo Express to view and manage your database.


## Technologies Used

* [Streamlit](https://streamlit.io/) — Web App Framework
* [MongoDB](https://www.mongodb.com/) — NoSQL Database
* [Mongo Express](https://github.com/mongo-express/mongo-express) — Web UI for MongoDB
* [Docker](https://www.docker.com/) — Containerization
* [Docker Compose](https://docs.docker.com/compose/) — Multi-container Orchestration
* [YouTube Data API v3](https://developers.google.com/youtube/v3) — Fetching YouTube Channel and Video Data


## How It Works

* The **Streamlit app** collects user input (API Key + Channel ID) and fetches data from YouTube API.
* **Channel information** is stored in the `channels` collection in **MongoDB**.
* **Video list** is stored in the `videos` collection in **MongoDB**.
* **Mongo Express** provides a web interface to explore and manage the MongoDB collections.

