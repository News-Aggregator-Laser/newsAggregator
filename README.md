# Django News Aggregator Project

## Overview

This is a Django-based news aggregator web page that integrates multiple web crawlers to collect and display news from
various sources. It offers several features to enhance the user's experience, including the ability to filter news based
on the source, location, etc., personalize news viewing using AI algorithms, share news on social media, and comment on
news articles.

## Features:

- Filter news based on various criteria such as source, category, etc.
- Customized news viewing using AI algorithms, with news appearing based on the user's previous queries and viewing
  habits.
- Share news on social media.
- Comment on news articles.

## Project Structure

The project consists of several apps and packages, including:

- `api` Contains endpoints to access news data from multiple APIs, as well as functionalities such as adding,
  removing, liking, and commenting on news articles.
- `news` The main website, where users can view news articles, filter news based on various criteria, search for news,
  and share news on social media. The website also includes a "Your Feed" page that displays news articles based on the
  user's history and likes.
- `schedule_services` The task manager, which handles tasks such as archiving old news, sending daily emails to
  subscribers, and managing API requests.
- `ml_logic` A package containing machine learning algorithms used for generating tags for each news article,
  recommending news to the user, and analyzing and categorizing news articles.
- `static` A folder for storing static files such as images and CSS.
- `templates` A folder containing HTML templates and components for the website.

## Technologies and Algorithms Used

1. Django: The project is built using the Django framework, which provides a high-level Python web development
   framework.
2. JSON Path: Used to extract data from different APIs and store it in a common database.
3. Regex: Used for standardizing the author and source names in news articles.
4. Task Manager: To manage tasks such as archiving old news and sending daily emails to subscribers. The task manager is
   designed to run only once, using the WSGI file with caching.
5. Trend Analysis: The task manager uses trend analysis to determine the most popular news articles in a 24-hour period,
   which will be included in the daily email to subscribers.
6. Data Standardization: The project uses regex and other methods to standardize data from different APIs, such as
   replacing missing author or category information with "unknown" or "General".
7. Machine Learning: The project uses machine learning algorithms to generate tags for each news article, recommend news
   to the user based on similar tags and category, and analyze and categorize news articles.
8. Jazzmin: Used for customizing the Django admin panel.
9. Bootstrap icon: Used for styling the website.
10. Django REST Framework: Used for creating the API endpoints.
11. Django Social Share: Used for adding social media sharing buttons to the website.

## Requirements

To run the project, you will need to install the required packages in the requirements.txt file. You can do this by
running the following command:

```bash
pip install -r requirements.txt
```

## Conclusion

This Django project provides a comprehensive news aggregator solution, combining data from multiple APIs and using
machine learning algorithms for data analysis and categorization. The project is organized into several apps and
packages, making it easy to maintain and add new features in the future. With features such as filtering, searching, and
social media sharing, the project offers a user-friendly experience for accessing and interacting with news articles.