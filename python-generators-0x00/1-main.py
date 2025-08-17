#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_to_prodev()
if connection:
    for user in seed.stream_user_data(connection):
        print(user)
    connection.close()

#!/usr/bin/python3
from itertools import islice
stream_users = __import__('0-stream_users').stream_users

# iterate over the generator function and print only the first 6 rows
for user in islice(stream_users(), 6):
    print(user)
