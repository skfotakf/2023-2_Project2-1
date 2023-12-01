import pymysql
import pandas as pd
from tabulate import tabulate

data = pd.read_csv("data.csv", encoding='utf-8')

conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='password',
        db='movieDB',
        charset='utf8'
    )
# Problem 1 (5 pt.)
def initialize_database():
    # YOUR CODE GOES HERE


    sql0 = "DROP DATABASE movieDB"
    sql1 = "CREATE DATABASE movieDB"
    sql2 = "USE movieDB"
    sql3 = """CREATE TABLE movie (
            id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            title varchar(255) NOT NULL UNIQUE KEY,
            director varchar(255) NOT NULL,
            price int(11) NOT NULL CHECK (price >= 0 AND price <= 100000 )
    )
    """
    sql4 = """create table user (
        id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name varchar(255) NOT NULL,
        age int(11) NOT NULL CHECK (age >= 12 AND age <= 110 ),
        UNIQUE(name, age)
    )
    """
    sql5 = """create table mov_user(
        mov_id int(11) NOT NULL,
        user_id int(11) NOT NULL,
        FOREIGN KEY (mov_id) REFERENCES movie(id),
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    """
    sql6 = "INSERT INTO movie(title, director, price) VALUES (%s, %s, %s);"
    sql7 = "INSERT INTO user(name, age) VALUES(%s, %s);"
    sql8 = "INSERT INTO mov_user(mov_id, user_id) VALUES (%s, %s)"
    sql10 = "SELECT * FROM movie"


    with conn.cursor() as cur:
        cur.execute(sql0)
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        cur.execute(sql4)
        cur.execute(sql5)

        movieData = []
        userData = []
        movieList = []
        userList = []

        for idx in range(len(data)):
            movieData.append([data.values[idx][0], data.values[idx][1], data.values[idx][2]])
            userData.append([data.values[idx][3], data.values[idx][4]])
            # cur.execute(sql6, (data.values[idx][0], data.values[idx][1], data.values[idx][2]))
            # cur.execute(sql7, (data.values[idx][3], data.values[idx][4]))

        for value in movieData:
            if value not in movieList:
                movieList.append(value)

        for value in userData:
            if value not in userList:
                userList.append(value)

        for value in movieList:
            cur.execute(sql6, (value[0], value[1], value[2]))

        for value in userList:
            cur.execute(sql7, (value[0], value[1]))

        for idx in range(len(data)):
            cur.execute(sql8, (movieList.index([data.values[idx][0], data.values[idx][1], data.values[idx][2]]) + 1,
                               userList.index([data.values[idx][3], data.values[idx][4]]) + 1))

        cur.execute(sql10)
        for result in cur:
            print(result)

    print('Database successfully initialized')
    # YOUR CODE GOES HERE
    pass


# Problem 15 (5 pt.)
def reset():
    # YOUR CODE GOES HERE

    # YOUR CODE GOES HERE
    pass


# Problem 2 (4 pt.)
def print_movies():
    # YOUR CODE GOES HERE
    sql1 = """SELECT movie.id, movie.title, movie.director, ROUND(AVG(movie.price)), COUNT(mov_user.mov_id)
            FROM movie
            LEFT JOIN mov_user on movie.id = mov_user.mov_id
            GROUP BY movie.id
    """
    with conn.cursor() as cur:
        cur.execute(sql1)
        results = cur.fetchall()
    conn.commit()

    table = [["id", "title", "director", "price", "count"]]
    for result in results:
        table.append(list(result))
    print(tabulate(table, headers='firstrow', tablefmt='psql'))

    # YOUR CODE GOES HERE
    pass


# Problem 3 (4 pt.)
def print_users():
    # YOUR CODE GOES HERE
    sql1 = "SELECT id, name, age FROM user ORDER BY id"

    with conn.cursor() as cur:
        cur.execute(sql1)
        results = cur.fetchall()
    conn.commit()

    table = [["id", "name", "age"]]
    for result in results:
        table.append(list(result))
    print(tabulate(table, headers='firstrow', tablefmt='psql'))

    # YOUR CODE GOES HERE
    pass


# Problem 4 (4 pt.)
def insert_movie():
    # YOUR CODE GOES HERE
    title = input('Movie title: ')
    director = input('Movie director: ')
    price = input('Movie price: ')

    sql1 = "INSERT INTO movie(title, director, price) VALUES(%s, %s, %s)"

    try:
        with conn.cursor() as cur:
            cur.execute(sql1, (title, director, price))
        conn.commit()

        print('One movie successfully inserted')


    except pymysql.err.IntegrityError:
        print(f'Movie {title} already exists')
    except pymysql.err.OperationalError:
        print('Movie price should be from 0 to 100000')

    pass

# Problem 6 (4 pt.)
def remove_movie():
    # YOUR CODE GOES HERE
    movie_id = input('Movie ID: ')

    sql0 = "SELECT id from movie where id = %s"
    sql1 = "DELETE FROM mov_user where mov_id = %s"
    sql2 = "DELETE FROM movie where id = %s"


    with conn.cursor() as cur:
        cur.execute(sql0, movie_id)
        if cur.fetchone() is None:
            print(f'Movie {movie_id} does not exist')
        else:
            cur.execute(sql1, movie_id)
            cur.execute(sql2, movie_id)
            print('One movie successfully removed')
    conn.commit()

    # YOUR CODE GOES HERE
    pass


# Problem 5 (4 pt.)
def insert_user():
    # YOUR CODE GOES HERE
    name = input('User name: ')
    age = input('User age: ')

    sql1 = "INSERT INTO user(name, age) VALUES(%s, %s)"

    try:
        with conn.cursor() as cur:
            cur.execute(sql1, (name, age))
        conn.commit()

        print('One user successfully inserted')

    except pymysql.err.IntegrityError:
        print(f'User ({name}, {age}) already exists')
    except pymysql.err.OperationalError:
        print('User age should be from 12 to 110')

    # YOUR CODE GOES HERE
    pass


# Problem 7 (4 pt.)
def remove_user():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')

    sql0 = "SELECT id from user where id = %s"
    sql1 = "DELETE FROM mov_user where user_id = %s"
    sql2 = "DELETE FROM user where id = %s"

    with conn.cursor() as cur:
        cur.execute(sql0, user_id)
        if cur.fetchone() is None:
            # error message
            print(f'User {user_id} does not exist')
        else:
            cur.execute(sql1, user_id)
            cur.execute(sql2, user_id)
            # success message
            print('One user successfully removed')
    conn.commit()


    # YOUR CODE GOES HERE
    pass


# Problem 8 (5 pt.)
def book_movie():
    # YOUR CODE GOES HERE
    movie_id = input('Movie ID: ')
    user_id = input('User ID: ')

    # error message
    print(f'Movie {movie_id} does not exist')
    print(f'User {user_id} does not exist')
    print(f'User {user_id} already booked movie {movie_id}')
    print(f'Movie {movie_id} has already been fully booked')

    # success message
    print('Movie successfully booked')
    # YOUR CODE GOES HERE
    pass


# Problem 9 (5 pt.)
def rate_movie():
    # YOUR CODE GOES HERE
    movie_id = input('Movie ID: ')
    user_id = input('User ID: ')
    rating = input('Ratings (1~5): ')

    # error message
    print(f'Movie {movie_id} does not exist')
    print(f'User {user_id} does not exist')
    print(f'Wrong value for a rating')
    print(f'User {user_id} has not booked movie {movie_id} yet')
    print(f'User {user_id} has already rated movie {movie_id}')

    # success message
    print('Movie successfully rated')
    # YOUR CODE GOES HERE
    pass


# Problem 10 (5 pt.)
def print_users_for_movie():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')

    # error message
    print(f'User {user_id} does not exist')
    # YOUR CODE GOES HERE
    pass


# Problem 11 (5 pt.)
def print_movies_for_user():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')

    # error message
    print(f'User {user_id} does not exist')
    # YOUR CODE GOES HERE
    pass


# Problem 12 (6 pt.)
def recommend_popularity():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')

    # error message
    print(f'User {user_id} does not exist')
    # YOUR CODE GOES HERE
    pass


# Problem 13 (10 pt.)
def recommend_item_based():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')
    rec_count = input('Recommend Count: ')

    # error message
    print(f'User {user_id} does not exist')
    print('Rating does not exist')
    # YOUR CODE GOES HERE
    pass


# Total of 70 pt.
def main():
    while True:
        print('============================================================')
        print('1. initialize database')
        print('2. print all movies')
        print('3. print all users')
        print('4. insert a new movie')
        print('5. remove a movie')
        print('6. insert a new user')
        print('7. remove an user')
        print('8. book a movie')
        print('9. rate a movie')
        print('10. print all users who booked for a movie')
        print('11. print all movies booked by an user')
        print('12. recommend a movie for a user using popularity-based method')
        print('13. recommend a movie for a user using user-based collaborative filtering')
        print('14. exit')
        print('15. reset database')
        print('============================================================')
        menu = int(input('Select your action: '))

        if menu == 1:
            initialize_database()
        elif menu == 2:
            print_movies()
        elif menu == 3:
            print_users()
        elif menu == 4:
            insert_movie()
        elif menu == 5:
            remove_movie()
        elif menu == 6:
            insert_user()
        elif menu == 7:
            remove_user()
        elif menu == 8:
            book_movie()
        elif menu == 9:
            rate_movie()
        elif menu == 10:
            print_users_for_movie()
        elif menu == 11:
            print_movies_for_user()
        elif menu == 12:
            recommend_popularity()
        elif menu == 13:
            recommend_item_based()
        elif menu == 14:
            print('Bye!')
            break
        elif menu == 15:
            reset()
        else:
            print('Invalid action')


if __name__ == "__main__":
    main()
