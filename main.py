import requests
import json
import psycopg2
#
def getConnection(database, username, password, host, port):
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=host,
        port=port
    )
    return conn

#insertion of user and subscription
def insertIntoUser(conn, user):
    # users
    id = (-1 if user['id'] is None else int(user['id']))
    firstName = ("" if user['firstName'] is None else user['firstName'])
    lastName = ("" if user['lastName'] is None else user['lastName'])
    address = ("" if user['address'] is None else user['address'])
    city = ("" if user['city'] is None else user['city'])
    country = ""+("" if user['country'] is None else user['country'])
    zipCode = ("" if user['zipCode'] is None else user['zipCode'])
    email = ("" if user['email'] is None else user['email'])
    birthDate = ("" if user['birthDate'] is None else user['birthDate'])
    gender = ("" if user['profile']['gender'] is None else user['profile']['gender'])
    isSmoking = ("" if str(user['profile']['isSmoking']) is None else str(user['profile']['isSmoking']))
    profession = ("" if user['profile']['profession'] is None else user['profile']['profession'])
    income = (0.0 if user['profile']['income'] is None else float(user['profile']['income']))
    createdAt = ("" if user['createdAt'] is None else user['createdAt'])
    updatedAt = ("" if user['updatedAt'] is None else user['updatedAt'])
    cur = conn.cursor()
    cur.execute("delete from subscriptions where exists (select 1 from subscriptions a where a.userid=%s and a.userupdatedat<=%s)",(str(id), str(updatedAt)))
    cur.execute("delete from users where exists (select 1 from users a where a.id=%s and a.updatedAt<=%s)",(str(id),str(updatedAt)))
    cur.execute("insert into users (id,firstName,lastName,address,city,country,zipCode,email,birthDate,gender,isSmoking,profession,income,createdAt,updatedAt)"
               " values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(id),str(firstName),str(lastName),str(address),str(city),str(country),str(zipCode),str(email),str(birthDate),str(gender),str(isSmoking),str(profession),str(income),str(createdAt),str(updatedAt)))
    if bool(user['subscription'] ):
        for subscription in user['subscription']:
            subCreatedAt= ("" if subscription['createdAt'] is None else subscription['createdAt'])
            subStartDate= ("" if subscription['startDate'] is None else subscription['startDate'])
            subEndDate= ("" if subscription['endDate'] is None else subscription['endDate'])
            status= ("" if subscription['status'] is None else subscription['status'])
            amount=(0.0 if subscription['amount'] is None else float(subscription['amount']))
            cur.execute("insert into subscriptions (userId,startDate,endDate,status,amount,createdAt,userUpdatedAt) values (%s,%s,%s,%s,%s,%s,%s)",(str(id),str(subStartDate),str(subEndDate),str(status),str(amount),str(subCreatedAt),str(updatedAt)))
    conn.commit()

#insertion of messages
def insertIntoMessage(conn, message):

    id = (-1 if message['id'] is None else int(message['id']))
    senderId = (-1 if message['senderId'] is None else int(message['senderId']))
    receiverId = (-1 if message['receiverId'] is None else int(message['receiverId']))
    #msg = ("" if message['message'] is None else message['message'])
    createdAt = ("" if message['createdAt'] is None else message['createdAt'])
    cur = conn.cursor()
    cur.execute("insert into messages (id,senderId,receiverId,createdAt) select %s as id ,%s as senderId,%s as receiverId,%s as createdAt from messages where not exists (select 1 from messages where id=%s and senderId=%s and receiverId=%s and createdAt=%s)",(str(id),str(senderId),str(receiverId),str(createdAt),str(id),str(senderId),str(receiverId),str(createdAt)))
    conn.commit()




def main(name):
    print("Tables processing started ...")
    database="postgres"
    username="postgres"
    password="root"
    host="localhost"
    port="5432"
    users=requests.get("https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/users")
    messages=requests.get("https://619ca0ea68ebaa001753c9b0.mockapi.io/evaluation/dataengineer/jr/v1/messages")
    UsersJson = json.loads(users.text)
    MessagesJson = json.loads(messages.text)
    conn = getConnection(database, username, password, host, port)
    for user in UsersJson :
        insertIntoUser(conn,user)

    for message in MessagesJson :
        insertIntoMessage(conn, message)
    print("Tables processing completed ...!!!")

# install requests ,psycopg2
if __name__ == '__main__':
    main('PyCharm')

