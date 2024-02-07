import argparse
import csv
import sqlite3
import shutil
import os
import sys

#If XPdb path isn't provided, try to acquire
def acquire_xpdb():
	try:
		shutil.copyfile("/var/protected/xprotect/XPdb","./XPdb")
	except PermissionError as e:
		print(e)
		print("Are you running as root?")
		sys.exit()

#Get schema of XPdb because there might be different versions in the future
def get_schema_columns(xpdb):
	con = sqlite3.connect(xpdb)
	cur = con.cursor()
	cur.execute("PRAGMA table_info(events)")
	res = cur.fetchall()
	con.close()
	return [x[1] for x in res]

#Get the events from XPdb, returns a list of dictionaries
def get_events(xpdb, schema_columns):
	con = sqlite3.connect(xpdb)
	cur = con.cursor()

	#Get databaseSchemaVersion
	cur.execute("SELECT * FROM settings;")
	ver_tup = cur.fetchone()

	#Get events
	cur.execute("SELECT * FROM events;")
	res = cur.fetchall()
	event_dict_list = []
	for event in res:
		event_dict = {ver_tup[0]:ver_tup[1]}
		for i in range(len(schema_columns)):
			event_dict.update({schema_columns[i]:event[i]})
		event_dict_list.append(event_dict)
	return event_dict_list

#Write events to csv
def write_csv(events, output_csv, hostname):
	with open(output_csv, 'w', newline='') as csv_file:
		schema_columns = list(events[0].keys())
		schema_columns.append("hostname")
		writer = csv.DictWriter(csv_file, fieldnames=schema_columns)

		writer.writeheader()
		for event in events:
			event.update({"hostname":hostname})
			writer.writerow(event)


if __name__=="__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('--file', '-f', help='input file (xpdb)')
	parser.add_argument('--output', '-o', default="XPdb.csv", help='output csv file')
	parser.add_argument('--hostname', '-hn', help="source hostname of the XPdb if parsing offline, if not provided it will use the hostname of the current system")

	args = parser.parse_args()

	if args.file:
		XPdb_path = args.file
	else:
		XPdb_path = "./XPdb"
		acquire_xpdb()

	if args.hostname:
		hostname = args.hostname
	else:
		hostname = os.uname().nodename

	schema_columns = get_schema_columns(XPdb_path)
	events = get_events(XPdb_path,schema_columns)
	write_csv(events, args.output, hostname)

	try:
		os.remove("./XPdb")
	except:
		pass