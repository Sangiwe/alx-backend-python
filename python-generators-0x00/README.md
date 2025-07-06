# 0. Getting started with Python generators

## 📚 Objective

Create a generator that streams rows from a MySQL database one by one.

---

## 📁 Files

- `seed.py`: Sets up the MySQL database `ALX_prodev`, creates a table `user_data`, and inserts data from a CSV file.
- `0-main.py`: A sample script that runs the functions in `seed.py` to test the database and table setup.
- `user_data.csv`: Sample data to be inserted into the MySQL database.

---

## 🔧 Function Prototypes

### In `seed.py`:

- `def connect_db()`:  
  Connects to the MySQL server (without selecting a database).

- `def create_database(connection)`:  
  Creates the database `ALX_prodev` if it does not already exist.

- `def connect_to_prodev()`:  
  Connects to the `ALX_prodev` database.

- `def create_table(connection)`:  
  Creates the `user_data` table with the fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, Not Null)
  - `email` (VARCHAR, Not Null)
  - `age` (DECIMAL, Not Null)

- `def insert_data(connection, csv_file)`:  
  Inserts rows from the `user_data.csv` file into the table (only if the email doesn't already exist).

---

## 🛠️ Usage

```bash
# Make sure MySQL server is running
# Run the main script to test setup:
$ ./0-main.py
