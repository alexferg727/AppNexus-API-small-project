import requests
from bs4 import BeautifulSoup
from datetime import date

result = 'English HW:'

def getDate():

    today = date.today()
    today = today.strftime("%b-%d-%Y")
    today_month, today_day = today.split('-')[0], today.split('-')[1]

    return today_month, today_day

def compare_date(due):

    today_month, today_day = getDate()

    day, month = due.split('-')[0], due.split('-')[1]

    months = {
        'Jan' : 1,
        'Feb' : 2,
        'March' : 3,
        'Sep' : 9,
        'Oct' : 10,
        'Nov' : 11,
        'Dec' : 12
    }

    if (months[today_month] < months[month]) or (months[today_month] == months[month] and today_day <= day):
        return True

def main(email, password):

    result = 'English HW:'

    login_url = 'https://www.turnitin.com/login_page.asp?lang=en_us'


    #START A SESSION FOR THE LOGIN PAGE, BECAUSE IT WILL HAVE COOKIES WHICH REMEMBERS YOUR LOGIN FOR EVERY SESSION
    with requests.session() as client:

        #INITIALISE ASSIGNMENTS LIST, DATES AND CLASS LISTS TO BE USED LATER
        assignment_list = []
        due_dates = []
        class_links = []
        
        #GET SESSION ID AND INITIALISE CREDENTIALS
        client.get(login_url)
        session_id = client.cookies['session-id']
        login_data = {'email': email, 'user_password' : password, 'session-id' : session_id}
        
        #LOG INTO TURNITIN.COM
        print(session_id)
        r1 = client.post(login_url, data=login_data)

        print(r1.status_code)

        #REPLACE SESSION ID WITH CURRENT ONE POST LOGIN
        session_id = client.cookies['session-id']
        soup = BeautifulSoup(r1.content, 'html5lib')
        print(r1.text)

        #GET TABLE
        classes = soup.find('table')
        

        #GET LINKS FOR CLASSES IN TABLE

        try:
            for row in classes.find_all('td', class_='class_name'):
                class_links.append(row.find('a').get('href'))

        except AttributeError:
            return 'Wrong login'

        #GET ASSIGNMENTS AND DUE DATES FROM EVERY LINK
        for link in class_links:

            course_link = 'https://www.turnitin.com/' + link
            course = requests.get(course_link, params=({'session-id' : session_id}))
            soup = BeautifulSoup(course.content, 'html5lib')

            #SCRAPE WEBSITE FOR ASSIGNMENT TITLE
            for assignment in soup.find('table', id="student_assignment_table").find_all('div', class_='assignment-title'):
                assignment_list.append(assignment.text)

            #THEN SCRAPE IT FOR THE DATES
            for dates in soup.find_all('div', class_='dates'):
                due = dates.find('div', class_='date due-date').text

                if compare_date(due):
                    due_dates.append(due)
 
        # OUTPUT THEM UNDER THE ASSUMPTION THEY ARE PARALLEL
        for i, v in zip(reversed(assignment_list), reversed(due_dates)):

            result += f'\n{v} : {i}'
    
    return result

if __name__ == '__main__':

    print(main('alex.fer@student.mahidol.edu', ''))
