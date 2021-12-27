import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


con = sqlite3.connect('works.sqlite')
cursor = con.cursor()
cursor.execute('drop table if exists works')
cursor.execute('create table works ('
               'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
               'salary INTEGER,'
               'educationType TEXT,'
               'jobTitle TEXT,'
               'qualification TEXT,'
               'gender TEXT,'
               'dateModify TEXT,'
               'skills TEXT,'
               'otherInfo TEXT)')
con.commit()

df = pd.read_csv("works.csv")
df.to_sql("works", con, if_exists='append', index=False)
con.commit()


cursor.execute('create index salary_index on works (salary)')
con.commit()


cursor.execute('SELECT count(*) FROM works')
print(cursor.fetchall()[0][0])


cursor.execute("SELECT gender, count(*) FROM works GROUP BY works.gender")
print(cursor.fetchall())


cursor.execute("SELECT count(*) FROM works WHERE works.skills IS NOT NULL")
print(cursor.fetchall()[0][0])


cursor.execute("SELECT * FROM works WHERE works.skills IS NOT NULL")
print(cursor.fetchall())


cursor.execute("SELECT salary FROM works WHERE skills LIKE '%Python%'")
print(cursor.fetchall())


cursor.execute("SELECT salary FROM works WHERE gender = 'Мужской'")
m_salary = [i[0] for i in cursor.fetchall()]
cursor.execute("SELECT salary FROM works WHERE gender = 'Женский'")
w_salary = [i[0] for i in cursor.fetchall()]

m_quantile = np.quantile(m_salary, np.linspace(0.1, 1, 10))
w_quantile = np.quantile(w_salary, np.linspace(0.1, 1, 10))
plt.hist(m_quantile, 100, color='blue')
plt.show()
plt.hist(w_quantile, 100, color='red')
plt.show()
con.commit()
