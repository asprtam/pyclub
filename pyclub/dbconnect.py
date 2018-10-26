import pymysql
from pymysql import escape_string
from flask_login._compat import unicode
from datetime import datetime, timedelta

__author__ = "Tomasz Lakomy"

def create_db():
	"""Function creates database from file create-database_pyclub.py"""
	c, conn = connection()
	c.execute("SOURCE sql/create-database_pyclub.sql")
	c.close()
	conn.close()

def connection():
	"""Function connects to database"""
	conn = pymysql.connect(host='localhost',
			       user='kostek',
			       password='',
			       db='pyclub',
			       charset='utf8mb4',
			       cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn

def create_user(first_name, last_name, email, password):
	"""Function creates user"""
	c, conn = connection()
	c.execute("INSERT INTO user (first_name, last_name, email, password, email_confirm) VALUES"
			  "(%s, %s, %s, %s, 0)"
			  , (escape_string(first_name), escape_string(last_name), escape_string(email), escape_string(password))
	)
	conn.commit()
	c.close()
	conn.close()

def create_organization(name, contact):
	"""Function creates organization"""
	c, conn = connection()
	c.execute("INSERT INTO organization (name, contact) VALUES"
			  "(%s, %s)"
			  , (escape_string(name), escape_string(contact))
	)
	conn.commit()
	c.close()
	conn.close()

def create_club(info, organization_id):
	"""Function creates club"""
	c, conn = connection()
	c.execute("INSERT INTO club (info, organization_id) VALUES"
			  "(%s, %s)"
			  , (escape_string(info), escape_string(str(organization_id)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_event(date, info, club_id):
	"""Function creates event"""
	c, conn = connection()
	c.execute("INSERT INTO event (date, info, club_id) VALUES"
			  "(%s, %s, %s)"
			  , (escape_string(str(date)), escape_string(info), escape_string(str(club_id)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_event_membership(userid, eventid):
	"""Function takes user id, event id and club which is owner of the event and assigns user to event"""
	c, conn = connection()
	c.execute('INSERT INTO event_membership (user_id, event_id) VALUES'
			  '(%s, %s)'
			  , (escape_string(str(userid)), escape_string(str(eventid)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_club_membership(userid, clubid):
	"""Function takes user id and club id and assigns user to that club"""
	c, conn = connection()
	c.execute('INSERT INTO club_membership (user_id, club_id) VALUES'
			  '(%s, %s)'
			  , (escape_string(str(userid)), escape_string(str(clubid)))
	)
	conn.commit()
	c.close()
	conn.close()

def del_user(userid):
	c, conn = connection()
	c.execute('DELETE from user WHERE iduser=%s;', (escape_string(str(userid))))
	conn.commit()
	c.close()
	conn.close()

def del_organization(organizationid):
	c, conn = connection()
	c.execute('DELETE from organization WHERE idorganization=%s;', (escape_string(str(organizationid))))
	conn.commit()
	c.close()
	conn.close()

def del_club(clubid):
	c, conn = connection()
	c.execute('DELETE from club WHERE idclub=%s;', (escape_string(str(clubid))))
	conn.commit()
	c.close()
	conn.close()

def del_event(eventid):
	c, conn = connection()
	c.execute('DELETE from event WHERE idevent=%s;', (escape_string(str(eventid))))
	conn.commit()
	c.close()
	conn.close()

def get_user(userkey):
	"""Function takes user's id or user's email and returns dict with data from database"""
	c, conn = connection()
	c.execute("SELECT * FROM user WHERE iduser=%s or email=%s", (escape_string(str(userkey)), escape_string(str(userkey))))
	execute = (c.fetchone())
	if execute is None:
		return None
	user_data = User()
	user_data.update(execute)
	c.close()
	conn.close()
	user_data.id = user_data['iduser']
	return user_data

class User(dict):
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymus(self):
		return True
	def get_id(self):
		return unicode(self['iduser'])
	def userid(self, userkey):
		self.id = userkey

def get_organization(organizationkey):
	"""Function returns organization data"""
	c, conn = connection()
	c.execute("SELECT * FROM organization WHERE idorganization=%s or name=%s", (escape_string(str(organizationkey)), escape_string(organizationkey)))
	organization_data = c.fetchone()
	c.close()
	conn.close()
	return organization_data

def get_club(clubid):
	"""Function takes club id and returns club data"""
	c, conn = connection()
	c.execute("SELECT * FROM club WHERE idclub=%s", (escape_string(str(clubid))))
	club_data = c.fetchone()
	c.close()
	conn.close()
	return club_data

def get_event(eventid):
	"""Functions takes event id and returns event data"""
	c, conn = connection()
	c.execute("SELECT * FROM event WHERE idevent=%s", (escape_string(str(eventid))))
	event_data = c.fetchone()
	c.close()
	conn.close()
	return event_data

def get_event_membership(eventid):
	"""Function takes userid or eventid and returns event membership"""
	c, conn = connection()
	c.execute('SELECT * FROM event_membership WHERE event_id=%s', (escape_string(str(eventid))))
	eventid = c.fetchall()
	c.close()
	conn.close()
	return eventid

def get_user_to_event_membership(userid):
	c, conn = connection()
	c.execute('SELECT * FROM event_membership WHERE user_id=%s', (escape_string(str(userid))))
	userid = c.fetchall()
	c.close()
	conn.close()
	return userid

def get_club_membership(clubid):
	"""Function takes clubid and returns club membership"""
	c, conn = connection()
	c.execute('SELECT * FROM club_membership WHERE club_id=%s', (escape_string(str(clubid))))
	clubid = c.fetchall()
	c.close()
	conn.close()
	return clubid

def get_user_to_club_membership(userid):
	c, conn = connection()
	c.execute('SELECT * FROM club_membership WHERE user_id=%s', (escape_string(str(userid))))
	userid = c.fetchall()
	c.close()
	conn.close()
	return userid

def confirm_email(usermail):
	'''Function confirms user's mail'''
	c, conn = connection()
	c.execute('UPDATE user SET email_confirm=1 WHERE email=%s', (escape_string(usermail)))
	conn.commit()
	c.close()
	conn.close()


def get_event_next_week():
	"""Functions shows events from the next week

			returns: list with events planned to next week
	"""
	today = datetime.today()
	weekday = today.weekday()
	days_to = 6 - weekday
	start_time = today + timedelta(days=days_to)
	end_time = start_time + timedelta(days=7)
	c, conn = connection()
	c.execute('SELECT idevent FROM event WHERE date>%s and date<=%s', (start_time, end_time))
	event_data = c.fetchall()
	c.close()
	conn.close()
	return event_data
print(get_event_next_week())
def get_event_current_week():
	"""Functions shows events from the current week
	
			returns: list with events planned to current week
	"""
	today = datetime.today()
	weekday = today.weekday()
	days_left = 6-weekday
	time = today + timedelta(days=days_left)
	c, conn = connection()
	c.execute('SELECT idevent FROM event WHERE date<%s and date>%s', (time, today))
	event_data = c.fetchall()
	c.close()
	conn.close()
	return event_data

def get_event_next_month():
	"""Functions shows events from the current week
	
			returns: list of events planned to next month
	"""
	today = datetime.today()
	time = today + timedelta(days=30)
	c, conn = connection()
	c.execute('SELECT idevent FROM event WHERE date<=%s and date>%s', (time, today))
	event_data = c.fetchall()
	c.close()
	conn.close()
	return event_data
