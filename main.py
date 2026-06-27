import datetime as dt
import pandas
import smtplib
from email.mime.text import MIMEText


today = dt.datetime.now()
m = today.month
d = today.day

with open("birthdays.csv", encoding="utf-8") as f:
    data = pandas.read_csv(f)

birthday_people = data.query('month == @m and day == @d')
try:
    new_names = [birthday_people["name"].item()]
except ValueError:
    new_names = [n[1]["name"] for n in birthday_people.iterrows()]
print(birthday_people)
print(new_names)

###

with open("Letter.txt", "r", encoding="utf-8") as f:
    letter = f.read()
    letters = []
    for name in new_names:
        new = letter.replace("[NAME]", name)
        letters.append(new)
    dic_letters = dict(zip(new_names, letters))
    print(dic_letters)


my_email = "EMAIL"
psw = "PASSWORD"
with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls() # this encrypts the email in case it is intercepted
    connection.login(my_email, psw)
    for n in dic_letters:
        email = birthday_people.query("name == @n")["email"].item()
        msg = MIMEText(f"{dic_letters[n]}", "plain", "utf-8")
        msg["Subject"] = "Birthday"
        msg["From"] = my_email
        msg["To"] = email
        connection.sendmail(msg["From"], msg["To"], msg.as_string())
