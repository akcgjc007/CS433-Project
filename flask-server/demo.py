from DbStreamer.main import *
from data import *

obj = DbStreamer()

n = 5
users = [
    ["james554", "James", "james@gmail.com", "0000"],
    ["thomas999", "Thomas", "thomas@gmail.com", "0000"],
    ["harry555", "Harry", "harry@gmail.com", "0000"],
    ["vivek999", "Vivek", "vivek@gmail.com", "0000"],
    ["anupam110", "Anupam", "anupam@gmail.com", "0000"],
]

for user in users:
    obj.insert_into_users(user[0], user[1], user[2], user[3])

total_answers = 0
for i in range(n):
    obj.insert_into_questions(titles[i], descriptions[i], users[i][0])
    obj.upvote_question(users[i][0], i+1)

    for answer in answers[i]:
        obj.insert_into_answers(answer, i+1, users[i][0])
        total_answers += 1
        obj.upvote_answer(users[i][0], total_answers)

    for tag in tags[i]:
        obj.insert_into_tags(tag, i+1)

# obj.update_question(1, "dummpy question description")
# obj.update_answer(1, "dummy answer description")
# obj.delete_question(1)
# obj.delete_answer(1)


print(obj.search_question("dummy"))
print(obj.search_answers(2))
print(obj.search_by_tag("py"))
print(obj.search_question_by_id(2))
print(obj.get_top_questions())

print(obj.check_user("a@iitgn.ac.in", "abcd"))
obj.insert_into_tokens("james554", "1e758b81-fc45-467f-b375-2b6a218048c5")
print(obj.check_token("2e758b81-fc45-467f-b375-2b6a218048c5"))

print(obj.calc_reputation("thomas999"))
