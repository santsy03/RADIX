import smtplib
from datetime import datetime
from ussd.metrics.config import mailServerTimeTemplate,mailServerTemplate
from ussd.metrics.sendmetric import sendMetric

def sendEmail(resources): 
    msisdn = resources['parameters']['msisdn']
    amount = resources['parameters']['amount']
    email_to = 'Hanitiana.R@mg.airtel.com','faly.r@mg.airtel.com','121@mg.airtel.com','JEDIDIAR@mg.ibm.com','hasitiana.r@mg.airtel.com'
    email_user = 'ussd2.support@ke.airtel.com'
    email_subj = 'CL %s'%(str(msisdn))
    message = "Merci d'ajouter %s Ar a mon 'Credit Limit'"%(str(amount))
    try:
        #smtpserver = smtplib.SMTP("172.25.129.3",25,timeout=15)
        smtpserver = smtplib.SMTP("10.56.94.24",25,timeout=15)
        smtpserver.ehlo()
        header = 'To: %s \nFrom: %s \nSubject: %s \n'% (email_to, email_user, email_subj)
        msg = header + '\n %s \n\n'%(message)
        resources['type'] = 'timer'
        resources['start'] = datetime.now()
        resources['nameSpace'] = mailServerTimeTemplate
        smtpserver.sendmail(email_user, email_to, msg)
        smtpserver.close()
        sendMetric(resources)
    except Exception, e:
        print 'Failed sending email with error - %s'% (str(e))
        resources['parameters']['email_status'] = False
        resources['type'] = 'beat'
        action = 'failure'
        resources['nameSpace'] = mailServerTemplate.substitute(package=action)
        sendMetric(resources)
    else:
        resources['type'] = 'beat'
        action = 'success'
        resources['nameSpace'] = mailServerTemplate.substitute(package=action)
        sendMetric(resources)
        print 'Email successfully sent to %s'% (str(email_to))
        resources['parameters']['email_status'] = True
    return resources

if __name__ == '__main__':
    resources = {}
    resources['parameters'] ={} 
    resources['parameters']['msisdn'] = '261337272618'
    resources['parameters']['amount'] = '5000'
    sendEmail(resources)
