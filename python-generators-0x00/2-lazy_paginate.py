import seed

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    for row in rows:
        row["age"] = int(row["age"])
    connection.close()
    return rows


def lazy_pagination(page_size):
    offset = 0
    while True:  # ✅ One loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # ✅ Yield one page at a time
        offset += page_size
