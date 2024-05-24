BLACK_LIST = [
    "linkedin.com/in/sumit-singh-rawat-07322822a",
    "linkedin.com/in/kishor-kumar-sarkar",
    "linkedin.com/in/mount-hikers-5957a31b1",
    "linkedin.com/in/nutan-bhandari-7994a7208",
    "linkedin.com/in/akshatesh-kala-5432ba199",
    "linkedin.com/in/sameer615"
]



def send_mail(user_email,username):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from os import environ

    # Email configuration
    sender_email = environ.get('EMAIL')
    password = environ.get('GMAIL_APP_PASSWORD')

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = user_email
    message['Subject'] = 'Seeking Your Referral for Linux System Admin Opportunities'

    # Add body to email
    body = f'''
Hi {username},

    I hope you’re doing well. I’m reaching out because I recently graduated and am excited to begin my career as a Linux System Administrator.
Knowing your expertise and experience in the field, I thought to connect with you for guidance and support.

    I’m particularly interested in exploring opportunities at your current company, given its reputation for innovation and professional growth.
If there are any openings for Linux System Admin freshers, I would be incredibly grateful if you could refer me or provide some insight on how I might best approach applying.

    Your referral would mean a lot to me, as I highly respect your work and the path you've taken in your career. 
    Thank you so much for considering my request.

            

Best regards,
Dheeraj Kumar Roy
Mob: 9368449238
linkedin.com/in/dheerajkumar8855/
Dehradun, Uttarakhand

'''

    message.attach(MIMEText(body, 'plain'))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)  # Login to Gmail SMTP server
        text = message.as_string()
        server.sendmail(sender_email, user_email, text)  # Send the email


def SEND_EMAIL():
        #db action
        import time
        import sqlite3
        conn = sqlite3.connect('webSrapper.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Profile,Name, Email FROM webdata WHERE Email IS NOT NULL')
        profile = cursor.fetchall()
        conn.close()
        n=1
        for url,username,user_email in profile:
            try:
                if url in BLACK_LIST:
                    continue
                else:
                    send_mail(user_email,username)
                    time.sleep(2)
                    print(f'({n}) email sent to {username}: {user_email}')
                    n+=1
            except Exception as e:
                print(e)



