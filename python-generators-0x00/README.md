# Python Generators – Streaming SQL Data

This project demonstrates how to work with **Python generators** and **MySQL databases** by:

-   Seeding a MySQL database (`ALX_prodev`) with user data from a CSV file
-   Using a generator to **stream rows one-by-one** from the database
-   Avoiding loading all data into memory at once

---

## 🛠️ Project Structure

| File            | Description                                                                       |
| --------------- | --------------------------------------------------------------------------------- |
| `seed.py`       | Core logic to connect to MySQL, create database/table, seed data, and stream rows |
| `0-main.py`     | Script to set up the database and load user data                                  |
| `1-main.py`     | Script to test the generator that streams data                                    |
| `user_data.csv` | Sample user data used to populate the database                                    |

---

## 📂 Requirements

-   Python 3
-   MySQL installed (running locally)
-   `mysql-connector-python` package

Install connector:

```bash
pip3 install mysql-connector-python
```
