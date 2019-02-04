# Libraries
import smtplib
from email.message import EmailMessage
import imghdr

# Local code
from credentials import getEmailCredentials, defineImagemDir


def loginGmail():
    usr, pwd = getEmailCredentials()
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(usr, pwd)
        print('Logado no Gmail como {0}'.format(str(usr)))
    except:
        print('ocorreu um erro no LOGIN')
        raise
    return usr, server



def sendGmail(
        subject = 'default',
        body = 'Hey, whats up?\n\n- You',
        to = ''):
    """envia o e-mail usando as credenciais armazenadas em credentials.py
    recebe SUBJECT, BODY e TO.
    TO pode ser um e-mail só entre aspas, ou pode ser uma lista de e-mails"""

    # cria o SMTP server e traz o email da credencial
    msgfrom, server = loginGmail()

    # se TO vier vazio, mandar o email pra si mesmo
    if to == '':
        to = msgfrom
    if isinstance(to, (list,)):
        sendto = ", ".join(to)
    else:
        sendto = to
        

    # prepara a mensagem concatenando headers (modo plain text
    message = "From: %s\r\nTo: %s\r\nSubject: %s\n\n" % (msgfrom, sendto, subject)
    message += body
    try:
        server.sendmail(msgfrom, to, message)
        print('Email enviado para {0}'.format(str(sendto)))
    except:
        print('ocorreu um erro no ENVIO')
        raise
    server.quit()
    print('Conexao fechada como {0}'.format(str(msgfrom)))


# adiciona imagem
def MIMEaddImages(msg, diretorio, arquivo):
    with open(diretorio + arquivo, 'rb') as fp:
        img_data = fp.read()
    msg.add_attachment(img_data,
                       maintype='image',
                       subtype=imghdr.what(None, img_data),
                       filename=arquivo)
    return msg


def sendGmailMIME():
    # cria o SMTP server e traz o email da credencial
    msgfrom, server = loginGmail()
    localpath = defineImagemDir()

    msg = EmailMessage()
    msg.set_content('Hey, whats up?\n\n- You')
    msg['Subject'] = 'OMG Super Important Message 11'
    msg['From'] = msgfrom
    msg['To'] = msgfrom

    msg = MIMEaddImages(msg, diretorio=localpath, arquivo='blindar.png')
    msg = MIMEaddImages(msg, diretorio=localpath, arquivo='evoluir.png')

    # Envia a mensagem usando EmailMessage
    server.send_message(msg)
    print('Email enviado para {0}'.format(str(msgfrom)))

    # Fecha a conexao
    server.quit()



def sendGmailHTML():
    # cria o SMTP server e traz o email da credencial
    msgfrom, server = loginGmail()

    msg = EmailMessage()
    msg['Subject'] = 'OMG Super Important Message 13'
    msg['From'] = msgfrom
    msg['To'] = msgfrom

    # exemplo de HTML retirado de:
    # https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/
    msg.set_content("""\
    <html>
    <head>
        <title>A very simple webpage</title>
        <basefont size=4>
    </head>    
    <body bgcolor=FFFFFF>
        <h1>A very simple webpage. This is an "h1" level header.</h1>
        <h2>This is a level h2 header.</h2>
        <h6>This is a level h6 header.  Pretty small!</h6>
        <p>This is a standard paragraph.</p>
        <p align=center>Now I've aligned it in the center of the screen.</p>
        <p align=right>Now aligned to the right</p>
        <p><b>Bold text</b></p>
        <p><strong>Strongly emphasized text</strong>  Can you tell the difference vs. bold?</p>
        <p><i>Italics</i></p>
        <p><em>Emphasized text</em>  Just like Italics!</p>
        <p>Here is a pretty picture: <img src=https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/example/prettypicture.jpg alt="Pretty Picture"></p>
        <p>Same thing, aligned differently to the paragraph: <img align=top src=https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/example/prettypicture.jpg alt="Pretty Picture"></p>
        <hr>
        <h2>How about a nice ordered list!</h2>
        <ol>
            <li>This little piggy went to market
            <li>This little piggy went to SB228 class
            <li>This little piggy went to an expensive restaurant in Downtown Palo Alto
            <li>This little piggy ate too much at Indian Buffet.
            <li>This little piggy got lost
        </ol>
        <h2>Unordered list</h2>
        <ul>
            <li>First element
            <li>Second element
            <li>Third element
        </ul>    
        <hr>
        <h2>Nested Lists!</h2>
        <ul>
            <li>Things to to today:
                <ol>
                    <li>Walk the dog
                    <li>Feed the cat
                    <li>Mow the lawn
                </ol>
            <li>Things to do tomorrow:
                <ol>
                    <li>Lunch with mom
                    <li>Feed the hamster
                    <li>Clean kitchen
                </ol>
        </ul>
    
        <p>And finally, how about some <a href=http://www.yahoo.com/>Links?</a></p>
        <p>Remember, you can view the HTMl code from this or any other page by using the "View Page Source" command of your browser.</p>    
    </body>    
    </html>""", subtype='html')

    # Envia a mensagem usando EmailMessage
    server.send_message(msg)
    print('Email enviado para {0}'.format(str(msgfrom)))

    # Fecha a conexao
    server.quit()
