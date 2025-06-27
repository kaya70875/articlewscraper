# 🕷️ articlewscraper

A focused **web crawler microservice** built with **Scrapy** that scrapes and stores high-quality article content into a MongoDB database. Designed to integrate seamlessly with the main [`articlew`](https://github.com/kaya70875/articlew) project — an intelligent platform that generates sentence variations and educational content from real-world articles.

---

## 🚀 Project Purpose

This microservice is responsible for crawling articles from various sources (e.g., news, blogs, science) and saving structured sentence-level data to a MongoDB database. It offloads crawling and data collection tasks from the main app, allowing better separation of concerns and easier scaling.

> **Use Case**: Populate your database with fresh, real-world English sentences for educational, NLP, or machine learning purposes.

---

## 🛠️ Tech Stack

- **Scrapy** – For fast and flexible web crawling
- **MongoDB** – Stores parsed sentence-level data
- **Python 3.10+**
---

## ⚙️ How It Works

1. **Run a Spider**: Use Scrapy to start a crawl for a specific topic (e.g. science, news).
2. **Parse Articles**: Extracts article content and breaks them into individual sentences.
3. **Pipeline to MongoDB**: Sentences are pushed into your MongoDB collection in a structured format.
4. **Use in Main App**: The [`articlew`](https://github.com/kaya70875/articlew) app can query this data to generate educational content.

## Example Data Structure

{
  "sentence": "NASA announced a new Mars mission.",
  "source": "https://example.com/article/123",
  "category": "science",
  "created_at": "2025-06-27T12:00:00Z"
}
