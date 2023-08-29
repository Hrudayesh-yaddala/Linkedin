from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from fpdf import FPDF
import smtplib
import imghdr
from email.message import EmailMessage


print("finished importing required packages")
username='yaddalahrudayesh@gmail.com'
password='*******'
driver=webdriver.Chrome(executable_path='E:\\selenium_webdriver\\chromedriver')
sleep(1)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('Finished initializing a driver')
sleep(1)


driver.maximize_window()
email_field = driver.find_element_by_id('username')
email_field.send_keys(username)
sleep(1)

password_field = driver.find_element_by_name('session_password')
password_field.send_keys(password)
sleep(1)

signin_field=driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
sleep(1)
print('finised Login to Linkedin')


with open('profilelinks.txt','r') as inputfile:
    links=inputfile.readlines()
    for link in links:
        certificates=[]
        institute=[]
        skilist=[]
        driver.get(link)
        sleep(2)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find('div', {'class': 'mt2 relative'})
        sleep(2)
        # ************************scraping bio of the profile*************************************
        name_source=page_source.find('h1',class_='text-heading-xlarge inline t-24 v-align-middle break-words')
        name=name_source.getText().strip()
        descript_loc = info_div.find("div", {'class': 'text-body-medium break-words'})
        descript=descript_loc.getText().strip()
        locat_loc=info_div.find("span", {'class': 'text-body-small inline t-black--light break-words'})
        locat=locat_loc.get_text().strip()
        # *************************scraping candidate ceritfications**************************

        driver.get(link+'details/certifications/?profileUrn=urn%3Ali%3Afsd_profile%3AACoAACy8b4oBt7H2NvfVuEiLUDFWMIcaO54UeFw')
        sleep(2)
        cert_source = BeautifulSoup(driver.page_source, "html.parser")
        jobs = cert_source.find_all('div', class_ = 'pvs-list__container')
        for job in jobs[:100]:
            items = job.find_all('span', attrs = {'class' : 'mr1 hoverable-link-text t-bold'})
            institution=job.find_all('span', attrs = {'class' : 't-14 t-normal'})
            for i in range(len(items)):
                # print(items[i].text.strip())
                s=str(items[i].text.strip())
                certificates.append(s[0:(len(s)//2)])
            for i in range(len(institution)):
                s=str(institution[i].text.strip())
                institute.append(s[0:(len(s)//2)])
        #***********************************scraping candidate skill set ***************************************

        driver.get(link+'details/skills/')
        sleep(2)
        skill_source = BeautifulSoup(driver.page_source, "html.parser")
        jobs = skill_source.find_all('div', class_ = 'artdeco-tabs artdeco-tabs--size-t-48 ember-view')
        sleep(1)
        for job in jobs[:100]:
            items = job.find_all('span', attrs = {'class' : 'mr1 hoverable-link-text t-bold'})
            for i in range((len(items)//2)):
                s=str(items[i].text.strip())
                skilist.append(s[0:(len(s)//2)])

        with open('ouputresults.txt','a') as outputfile:
            sleep(1)
            outputfile.write(f'\nName  : {name}')
            outputfile.write(f'\nLocation  : {locat}\nAbout  : {descript}')
            outputfile.write('\nCERTIFICATIONS:')
            for i in range(len(certificates)):
                outputfile.write(f'\n{certificates[i]}---->({institute[i]})')
            outputfile.write('\nSKILLS:')
            for i in range(len(skilist)):
                outputfile.write(f'\n{skilist[i]}')
            outputfile.write('\n========================================= *END OF THE PROFILE* =====================================================================')
#***************************writing to pdf**************************

print('pdf initiated')
pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", size = 12)
f = open("ouputresults.txt", "r")
for x in f:
	pdf.cell(185, 10, txt = x, ln = 1, align = 'C')
pdf.output("candidate-profiles.pdf")
print('successfully pdf generated')

# ******************* sending email ************************************************


Sender_Email = "hrutestmail@gmail.com"
Reciever_Email='20bq1a4264@vvit.net'
Password = "pjstknutdzhwnqvd"

print('Email generation started')
newMessage = EmailMessage()                         
newMessage['Subject'] = "Check out the Candidates profile " 
newMessage['From'] = Sender_Email                   
newMessage['To'] = Reciever_Email                   
newMessage.set_content('Let me know what you think. Pdf attached!') 

files = ['candidate-profiles.pdf']

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name
    newMessage.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(Sender_Email, Password)              
    smtp.send_message(newMessage)    
    print('Email successfully sent')               
print('successfully program finished')
