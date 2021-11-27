
import socket
import threading
# from _thread import *
import pickle
from utils import *
from database import *
from datetime import datetime
import re


def logout_page(client_conn, database, username):
    """A function to logout client"""

    database[username]["is_logged"] = False

    # client_conn.send(
    # 	bytes(
    # 		"""You have been successfully logged out!
    # 			See you soon!
    # 		"""
    # 	, 'utf-8')
    # )

    client_conn.send(
        bytes(
            """You have been successfully logged out!
				See you soon!
				Where you want to see next?
				Reply with:
				1: Home Page
				2: Exit Page 
			""", 'utf-8')
    )

    response = client_conn.recv(1024).decode()

    if (response == "1"):
        home_page(client_conn, database)
        return
    elif(response == "2"):
        exit_page(client_conn)
        return
    return


def exit_page(client_conn):
    """ A function to send exit page to client"""
    client_conn.send(
        bytes(
            """Thanks for using Mini StackOverflow!""", 'utf-8')
    )
    return


def login_page(client_conn, database):
    """A function to send login page to client"""

    # while True:
    client_conn.send(
        bytes(
            """Enter your username and password:""", 'utf-8')
    )

    username = client_conn.recv(1024).decode()
    password = client_conn.recv(1024).decode()

    auth = login_auth(database, username, password)
    if (auth == 1):

        database[username]["is_logged"] = True

        client_conn.send(
            bytes(
                """Login Successful!
					Where you want to see next?
					Reply with:
					1: Profile page
					2: Log out (We will miss you!)
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if (response == "1"):
            user_profile_page(client_conn, database, username)
        elif (response == "2"):
            logout_page(client_conn, database, username)
            return
    elif (auth == 0):
        client_conn.send(
            bytes(
                """Login Unsuccessful! Please check your username
				Reply with:
				1: to create account
				2: to exit
				""", 'utf-8')
        )
        response = client_conn.recv(1024).decode()
        if (response == "1"):
            create_account_page(client_conn, database)
        elif (response == "2"):
            exit_page(client_conn)
            return
    else:
        client_conn.send(
            bytes(
                """Login Unsuccessful! Please check your password
				Reply with:
				1: to create account
				2: to exit
				""", 'utf-8')
        )
        response = client_conn.recv(1024).decode()
        if (response == "1"):
            create_account_page(client_conn, database)
        elif (response == "2"):
            exit_page(client_conn)
            return


def create_account_page(client_conn, database):
    """A function to handle create account messaging with client"""

    while True:
        client_conn.send(
            bytes(
                """Enter your username and password:""", 'utf-8')
        )

        username = client_conn.recv(1024).decode()
        password = client_conn.recv(1024).decode()

        # new function db_adduser
        database = db_adduser(database, username, password)
        print(database, "after login")

        client_conn.send(
            bytes(
                """
				Your account was made successfully!
				Reply with:
				1: to login
				2: to exit
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if (response == "1"):
            login_page(client_conn, database)
            return
        else:
            exit_page(client_conn)
            return


def home_page(client_conn, database):
    """A function to send home page to client"""

    while True:
        client_conn.send(
            bytes(
                """
				Reply with:
				1: Login
				2: Creating New Account
				3: Exit StackOverflow
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if not response:
            continue

        print(response)

        if (response == "1"):
            login_page(client_conn, database)
            return
        elif(response == "2"):
            create_account_page(client_conn, database)
            return
        elif (response == "3"):
            exit_page(client_conn)
            return


def user_profile_page(client_conn, database, username):
    """A function to send profile page to the client"""

    while True:
        # followers = db_get_user_followers(database, username)
        # followings = db_get_user_following(database, username)

        profile_message = """Your Profile details"""
        client_conn.send(
            bytes(
                """Your Profile details:
					\nUsername: 
				""" + username +
                """\nReputation: """ + Reputation +
                # """\nFollowers: """ + followers +
                # """\nFollowings:""" + followings +
                """\nReply with:
				1: Search Questions
				2: Your feed
				3: Your Questions
				4: Post Questions
				5: Search Tags
				6: Get Trending Tags
				7: Log out (We will miss you!)
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if (response == "1"):
            search_title_page(client_conn, database, username)
        elif (response == "2"):
            user_feed_page(client_conn, database, username)
        elif (response == "3"):
            user_questions_page(client_conn, database, username)
        elif (response == "4"):
            post_question(client_conn, database, username)
        elif (response == "7"):
            logout_page(client_conn, database, username)
            # return
        elif (response == "5"):
            search_tags(client_conn, database, username)
        elif(response == "6"):
            trending_hashtag(client_conn, database, username)


def search_title_page(client_conn, database, username):
    """A Function to send searched title/question to client"""

    while True:
        # allusers = db_get_all_users(database)   #### don't need this

        client_conn.send(
            bytes(
                # allusers + "\n" +   ### don't need this
                """Enter the username you want to search for:""", 'utf-8')
        )

        search_title = client_conn.recv(1024).decode()

        if (db_get_question(database, search_title)):
            # searched_question =
            client_conn.send(
                bytes(
                    """Question Found !
						Reply with:
						1: See Answers
						2: Post your answer
						3: Upvote Question
						4: To get all followings of searched user
						5: Your profile page
					""", 'utf-8')
            )

            response = client_conn.recv(1024).decode()

            if (response == "1"):
                see_answers(client_conn, database, search_title, username)
            elif (response == "2"):
                post_answer(client_conn, database, search_title, username)
            elif (response == "3"):
                upvote_question(client_conn, database, search_title)
            # elif (response == "4"):
                # user_followings_page(client_conn, database, search_user)
            elif (response == "5"):
                user_profile_page(client_conn, database, username)
        else:
            client_conn.send(
                bytes(
                    """User Not Found !
						Reply with:
						1: Your Profile page
					""", 'utf-8')
            )

            response = client_conn.recv(1024).decode()

            if (response == "1"):
                user_profile_page(client_conn, database, username)


def user_questions_page(client_conn, database, username):
    """A function to send page containing all its questions to client"""

    questions = db_get_user_questions(database, username)

    while True:
        client_conn.send(
            bytes(
                """Your Questions are:
				""" + questions +
                """ Enter Question to delete it
				""" +
                """or Reply with:
				1: Post Question
				2: Your profile page
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if (response == "1"):
            post_question(client_conn, database, username)
        elif (response == "2"):
            user_profile_page(client_conn, database, username)
        else:
            temp = db_delete_question(database, username, response)
            if (temp == 0):
                client_conn.send(bytes(
                    "The posted Question you entered do not exist. Reply with: 1: try again 2: Your profile page", 'utf-8'))
                response = client_conn.recv(1024).decode()
                if (response == "1"):
                    continue
                else:
                    user_profile_page(client_conn, database, username)
            else:
                database = temp
                client_conn.send(bytes(
                    "Question Deleted. Reply with: 1: Delete another 2: Your profile page", 'utf-8'))
                response = client_conn.recv(1024).decode()
                if (response == "1"):
                    continue
                else:
                    user_profile_page(client_conn, database, username)


def post_question(client_conn, database, username):
    """A function to send post question page to client"""
    while True:
        client_conn.send(
            bytes(
                """Enter Question to post""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

    # tweet=''
    # tweet_part=str((client_conn.recv(1024)).decode('utf-8'))
    # while tweet_part :
    # 	tweet+=tweet_part
    # 	tweet_part=str((client_conn.recv(1024)).decode('utf-8'))

        dt_object = datetime.now()
        date = dt_object.strftime("%d/%m/%Y")
        time = dt_object.strftime("%H:%M:%S")

        # creates a list of hashtags in the tweet
        hashtags = re.findall(r'#\w+', response)
        for hash in hashtags:
            database = db_setTags(database, hash, username,
                                  response, date, time, "NA")

        database = db_set_question(
            database, username, response, date, time, "NA")
        client_conn.send(
            bytes(
                """Question posted!
				Reply with:
				1: post another Question
				2: Your profile page
                3. Upvote Question
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if (response == "1"):
            post_question(client_conn, database, username)
        elif (response == "2"):
            user_profile_page(client_conn, database, username)
    # elif(response == "3"):
    #     upvote_question(client_conn,database,username)


def post_answer(client_conn, database, username):
    """A function to send post answer page to client"""
    while True:
        client_conn.send(
            bytes(
                """Enter Answer to post""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

    # tweet=''
    # tweet_part=str((client_conn.recv(1024)).decode('utf-8'))
    # while tweet_part :
    # 	tweet+=tweet_part
    # 	tweet_part=str((client_conn.recv(1024)).decode('utf-8'))

        dt_object = datetime.now()
        date = dt_object.strftime("%d/%m/%Y")
        time = dt_object.strftime("%H:%M:%S")

        database = db_set_answer(
            database, username, response, date, time, "NA")
        client_conn.send(
            bytes(
                """Question posted!
				Reply with:
				1: post another Answer
				2: Your profile page
                3. Upvote Answer
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if (response == "1"):
            post_question(client_conn, database, username)
        elif (response == "2"):
            user_profile_page(client_conn, database, username)


def upvote_question(client_conn, database, username):
    """A function to upvote a Question"""
    return None


def user_feed_page(client_conn, database, username):
    """To display client's questions and questions of other people client """

    print('feed')
    Questions = sorted(database[username]['tweets'], key=lambda i: (
        i['date'], i['time']), reverse=True)
    Questions = Questions[0:5]
    # followTweets=[]
    # for follow in database[username]['following']:
    # followTweets=sorted(database[follow]['tweets'],key =lambda i: (i['date'],i['time']),reverse=True)
    # Tweets.extend(followTweets[0:5])
    Questions = sorted(Questions, key=lambda i: (i['date'], i['time']))

    message = ''
    # Send Questions
    for que in Questions:
        message += "By "+username+" :-> " + \
            que['question'] + '\t'+que['date']+"  "+que['time']+'\n'
    # print(message)

    while True:
        client_conn.send(
            bytes(
                """Your Feed is:
				""" + """\n""" + message +
                """Reply with:
				1: Your profile page
				""", 'utf-8')
        )
        response = client_conn.recv(1024).decode()

        if (response == "1"):
            user_profile_page(client_conn, database, username)


# Searching for particular hashtag
def search_tags(client_conn, database, username):
    """A function to send search tags page to client"""
    while True:
        client_conn.send(
            bytes(
                """Enter a Tag to Search Question for it""", 'utf-8')
        )

        hash = client_conn.recv(1024).decode().replace('#', '')
        print(hash)
        hash = '#'+hash
        message = 'Search results for '+hash+'\n'
        if hash in database["hashtag_category"].keys():
            for h in database["hashtag_category"][hash]:
                message += "By "+h['username']+" :-> " + \
                    h['question'] + '\t'+h['date']+"  "+h['time']+'\n'

        else:
            message = hash+" Not Found"

        client_conn.send(
            bytes(
                message +
                """Reply with:
				1: Your profile page
				2: Search Tag
				""", 'utf-8')
        )

        response = client_conn.recv(1024).decode()

        if (response == "1"):
            user_profile_page(client_conn, database, username)
        elif (response == "2"):
            search_tags(client_conn, database, username)


# hostname and port number
host = "localhost"
port = 12345

# count for number of threads
thread_count = 0

# declaring socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

# listening for client
s.listen(5)
print('Server listening ... ')

while True:
    # got the connection from client
    connection, addr = s.accept()

    # connection.settimeout(10)
    database = db_load("user")

    home_page(connection, database)

    db_save(database, "user")
    print(" database saved")

    connection.close()
    print("connection closed", repr(addr))

# close the socket object
s.close()
