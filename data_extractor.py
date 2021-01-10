# CS 288 HW 8 Web Processing
# Jung Hyun Kim
# 12/1/2020 @ 0322

# This python code extracts data (which was downloaded in the bash script) using DOM,
#   and inserts the data into MySQL database

import sys
import os
import commands
import re
import MySQLdb

from xml.dom.minidom import parse, parseString

# For converting the dictionary to xml
from cStringIO import StringIO
from xml.parsers import expat



def get_elmnts_for_attr_value (tag, attr, value):
    lst = []
    final_lst = []

    # Get elements by 'tr'
    lst = dom.getElementsByTagName(tag)

    return lst


# Get all text recursively
def get_text(e):
    lst = []

    # Base case
    if e.nodeType in (3,4):
        lst.append(e.data)

    # Recursion
    else:
        child_list = e.childNodes
        for i in child_list:
            lst = lst + get_text(i)

    return lst


# Flatten a list
def flatten(f):

    return list(map(lambda x: x[0] if x else 'None', f))



# Replace whitespace characters
def replace_whitespace (str):
    p = re.compile(r'\s+')
    new = p.sub(' ', str)       # a lot of \n\t\t\t\t\t\t
    return new.strip()


# Replace but these characters including ':'
def replace_non_alpha_numeric (s):
    p = re.compile(r'[^a-zA-Z0-9:-]+')
    #    p = re.compile(r'\W+')   # replace whitespace characters
    new = p.sub(' ',s)
    return new.strip()


# Convert to xhtml
def html_to_xml(filename):
    # Run a shell command to run tagsoup
    os.system('java -jar tagsoup-1.2.1.jar --files ' +  filename) 

    # Save xhtml file name
    xhtml_file = filename.replace ('.html','.xhtml')

    # Make a copy of xhtml_file and name it index.html
    os.system("cp " + xhtml_file + " index.xhtml")

    return xhtml_file



# Extract values
def extract_values(dm):
    lst = []
    lst = get_elmnts_for_attr_value ('tr', 'class', 'most_actives')

    # Save the header row for creating a dictionary
    header = lst[0]

    # Get elements by 'th'
    headerElements = header.getElementsByTagName('th')
    headerText = list(map(lambda x: get_text(x), headerElements))
    
    # Flatten headerText list
    headerText = flatten(headerText)
    #print("Header row :")
    #print(headerText)
    #print("---------------------------------")

    # Delete header row from the table
    del lst[0]

    # Extract the values in the list
    lst = list(map(lambda tr: list(map(lambda x: get_text(x), tr.getElementsByTagName('td'))), lst))

    # Flatten the list
    lst = list(map(lambda x: flatten(x), lst))

    return lst



# Create dictionary
def toDictionary(values):
    # Manually create keys, because the header row contains % sign
    keys = ['Symbol', 'Name', 'Price', 'Chng', 'PercentChng', 'Volume', 'Avg_Volume_3mo', 'Market_Cap', 'PE_Ratio_TTM']

    return dict(map(lambda i: (keys[i], values[i]), range(len(keys))))




# Compose query to insert data into DB
def compose_query (tablename, dictionary):
    queries = []
    
    # Manually created keys
    keys = ['Symbol', 'Name', 'Price', 'Chng', 'PercentChng', 'Volume', 'Avg_Volume_3mo', 'Market_Cap', 'PE_Ratio_TTM']

    for i in range(len(dictionary)):
        current_dict = dictionary[i]
        queries.insert(i, 'INSERT INTO ' + tablename + ' (Symbol, Name, Price, Chng, PercentChng, Volume, Avg_Volume_3mo, Market_Cap, PE_Ratio_TTM) VALUES ("' + current_dict["Symbol"] + '","' + current_dict["Name"] + '","' + current_dict["Price"] + '","' + current_dict["Chng"] + '","' + current_dict["PercentChng"] + '","' + current_dict["Volume"] + '","' + current_dict["Avg_Volume_3mo"] + '","' + current_dict["Market_Cap"] + '","' + current_dict["PE_Ratio_TTM"] + '");')

    return queries



# mysql> describe most_active;
def insert_to_db (lst, tablename):

    # Intialize a cursor object
    cursor = db.cursor()

    # Create table
    create_table_string = 'CREATE TABLE ' + tablename + ' (Symbol varchar(10), Name varchar(80), Price varchar(20), Chng varchar(20), PercentChng varchar(20), Volume varchar(20), Avg_Volume_3mo varchar(20), Market_Cap varchar(20), PE_Ratio_TTM varchar(20));'
    cursor.execute(create_table_string)


    # Create a list of dictionaries
    list_dictionaries = list(map(lambda x: toDictionary(x), lst))
    ##DEBUG
    #for x in list_dictionaries: print(x)
    #first_dict = list_dictionaries[0]
    #print("Symbol of first dictionary is ---------------------")
    #print(first_dict["Symbol"])

    # Insert data into DB
    insert_query = compose_query (tablename, list_dictionaries)
    for i in insert_query:
        cursor.execute(i)

    cursor.close()
    db.commit()

    return 0



## Select DB from MySQL and display on terminal
#def select_from_db (tablename):
#
#    # Intialize a cursor object
#    cursor = db.cursor()
#
#    # code to show databases
#    showDB = "SHOW DATABASES;"
#    cursor.execute(showDB)    
#
#    # code to show tables
#    show_tables = "SHOW TABLES;"
#    cursor.execute(show_tables)
#
#    # code to display table
#    show_table = "SELECT * FROM " + tablename + ";"
#    cursor.execute(show_table)
#    # Fetch all rows of the resulting table
#    results = cursor.fetchall()
#    for row in results:
#        symbol = row[0]
#        name = row[1]
#        price = row[2]
#        chng = row[3]
#        percentchng = row[4]
#        volume = row[5]
#        avgvolume = row[6]
#        market_cap = row[7]
#        pe_ratio = row[8]
#
#        print("Symbol: %s, Name: %s, Price: %s, Change: %s, PercentChange: %s, Volume: %s, Avg Volume: %s, Market Cap: %s, PE_Ratio: %s" %(symbol, name, price, chng, percentchng, volume, avgvolume, market_cap, pe_ratio))
#
#
#    cursor.close()
#    db.commit()
#
#    return 0


# MAIN
def main():
    # Get filename from input
    html_filename = sys.argv[1]

    # Change filename extension from .html to .xhtml
    xhtml_filename = html_to_xml(html_filename)

    # Create a dom, then parse the .xhtml file
    global dom
    filename = "index.xhtml"
    dom = parse (filename)

    # Extract data from .xhtml file
    lst = extract_values (dom)

    # Drop filename extension to use it as table name in DB
    tablename = html_filename.replace('.html', '') 

    # Connect to MySQL database
    global db 
    db = MySQLdb.connect("localhost", "root", "snow5hite", "CS288")

    # Insert data into DB
    insert_to_db (lst, tablename)

    #select_from_db(tablename)

#    cursor = insert_to_db (lst, filename)   # filename = table name for MySQL

#    l = select_from_db(cursor, filename)    # display table on screen

    
    # Make sure Apache web server is up and running
    # Write a PHP script to display the table on browser

#    return xml
# end of main()

if __name__=="__main__":
    main()


# End of HW 8
