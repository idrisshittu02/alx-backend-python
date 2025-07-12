#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_to_prodev()
if connection:
    for user in seed.stream_user_data(connection):
        print(user)
    connection.close()
