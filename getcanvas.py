#Import libraries
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_assignments(link):

    #Get API
    params = 'include[]=assignments&include[]=all_dates'
    token1 = 'access_token=7~LtSZsf26rQd0IOVLkLv5p8nYd3CP5p9VNSzpBwc2Gc6CT1TTbYCSxpMZJWwrJwcY'
    due_dates = requests.get("{}?{}&{}".format(link, token1, params)).json()[:2]

    # soup = BeautifulSoup('canvas.html', 'html5lib')

    #Get assignments dictionary
    due = []
    for i in due_dates:
        due.append(i.get('assignments'))

    assignments = []

    today = str(datetime.today())[5:10]
    today_month, today_day = today[:2], today[3:]

    locks_at = []
    upcoming = ['Month  Day  Assignment']

    dates = {
        '01' : 'January',
        '02' : 'February',
        '03' : 'March',
        '04' : 'April',
        '05' : 'May',
        '06' : 'June',
        '07' : 'July',
        '08' : 'August',
        '09' : 'September',
        '10' : 'October',
        '11' : 'November',
        '12' : 'December',
    }

    #Get assignment names and due dates
    for i in range(len(due)):
        for j in range(len(due[i])):

            assignments.append(due[i][j].get('name') + ' : ' + due[i][j].get('lock_at'))

    #Separate upcoming assignments to finished ones
    for i in range(len(assignments)):

        due_at = assignments[i][len(assignments[i])-15:len(assignments[i]) - 10]
        month, day = due_at[:2], due_at[3:]

        if (today_month < month) or ((today_month == month) and today_day <= day):
            thing = assignments[i].split(' : ')
            upcoming.append("{}, {}, {}".format(dates.get(str(month)),day,thing[0]))

    result = ''

    for i in upcoming:
        # months = i.split(',')[0]
        # print(months)
        result += i + '\n'
    
    return result

print(get_assignments('https://canvas.instructure.com/api/v1/courses/5984515/assignment_groups') + '\n')
print(get_assignments('https://canvas.instructure.com/api/v1/courses/5983440/assignment_groups'))

    
#Print upcoming assignments in an easy to read manner
# # Create the table's column headers
# table = "<table>\n"

# # Create the table's column headers
# header = upcoming[0].split(",")
# table += "  <tr>\n"
# for column in header:
#     table += "    <th>{0}</th>\n".format(column.strip())
# table += "  </tr>\n"

# # Create the table's row data
# for line in upcoming[1:]:
#     row = line.split(",")
#     table += "  <tr>\n"
#     for column in row:
#         table += "    <td>{0}</td>\n".format(column.strip())
#     table += "  </tr>\n"

# table += "</table>"

# style = '''div{
#    width:200px;
#    height:125px;
#    padding:10px;
#    background-color:red;
#    border:1px solid black;
# }
# #circle {
#     background: lightblue;
#     border-radius: 50%;
#     width: 100px;
#     height: 100px;
# }
# p {
#   color : plum;
#   width: 500px;
#   border: 1px solid rgb(74, 23, 76);
#   text-align: end;
# }

# body {
#   width: 600px;
#   margin: 0 auto;
#   background-color: #575552;
#   padding: 0 50px 50px 50px;
#   border: 5px solid black;
# }

# html {
#   background-color: #00539f;
# }

# th {
#   color : rgb(0, 0, 0);
#   width: 500px;
#   text-align: start;
# }'''

# css = f'''<head>
# <style>
# {style}
# </style>
# </head>'''

# html_text = f"""<!DOCTYPE html>
# <html>
# <body>

# <h1>Physics: </h1>

# {table}

# {css}

# </body>
# </html>"""


# f = open('web_app.html', 'w')
# f.write(html_text)
# f.close()






    
    