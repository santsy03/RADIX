import re
import csv
import logging
import time
import datetime
from django import forms
#from django.utils import simplejson
import json
from django.db import connection
from django.contrib.auth import hashers
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from password_policies.models import PasswordHistory
from customerselfcare.forms import FrmThreeG
from common.config import opco, responses
from common.core import ServerError
from audittrail.views import perform_audit_trail


class CusPasswordChangeForm(PasswordChangeForm):
    MIN_LENGTH = 8
    final_password = ''

    def clean_new_password1(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(new_password) < self.MIN_LENGTH:
            raise forms.ValidationError('The new password must be at least %d '
                                        'characters long.' % self.MIN_LENGTH)

        # At least one letter and one non-letter
        first_isalpha = new_password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in new_password):
            raise forms.ValidationError('The new password must contain at '
                                        'least one letter and at least '
                                        'one digit.')

        # Can not change to same old as new
        if old_password == new_password:
            raise forms.ValidationError("You can not change to same old "
                                        "password.")

        # Mixed lower and upper case
        if new_password.islower() or new_password.isupper():
            raise forms.ValidationError("The password must contain both upper "
                                        "and lower cases.")

        # At least contain special characters
        if re.match("^[A-Za-z0-9_-]*$", new_password):
            raise forms.ValidationError("The password must contain special "
                                        "characters.")

        #Check has number
        if not any(char.isdigit() for char in new_password):
            raise forms.ValidationError("The new password must contain at "
                                        "least one Number.")

        # No character from username in password
        cur_uname = str(self.user)
        uname = list(cur_uname)
        wds, cnt, pwd_allowed = len(uname), 0, True
        for word in uname:
            pos = wds - cnt
            if pos > 3:
                uparts = cur_uname[cnt:][:3]
                if uparts in new_password:
                    pwd_allowed = False
            cnt += 1
        if not pwd_allowed:
            raise forms.ValidationError("The password can not contain part of "
                                        "your username.")

        if not PasswordHistory.objects.check_password(self.user, new_password):
            raise forms.ValidationError("The password has already been used.")

        self.final_password = new_password
        return new_password

    def save(self, commit=True):
        user = super(CusPasswordChangeForm, self).save(commit=commit)
        password = hashers.make_password(self.final_password)
        #After save delete expired
        print PasswordHistory.objects.create(user=user, password=password)
        print 'newton'
        print PasswordHistory.objects.delete_expired(user=user)
        return user


@login_required
def threeg(request):
    from common.core import get_subtype
    try:
        opco_code = opco['code']
        m_len = opco['mlen']
        if not request.session.get('user_full_names'):
            user_full_names = 'Admin'
        else:
            user_full_names = request.session['user_full_names']
        msg = ''
        response_data, result_list = {}, []
        if (request.method == 'POST'):
            subscriberno = str(request.POST.get('subscriberno'))
            subscribetoservice = str(request.POST.get('subscribetoservice'))
            if not subscribetoservice:
                msisdn = opco_code + str(subscriberno)[-m_len:]
                subscriberDetails = get_subtype(msisdn)
                #sub_type, balance = subscriberDetails.split(",")
                #sub_plans = Balance(msisdn)
                sub_type = subscriberDetails['sub_type']
                balance = subscriberDetails['ma_balance']
                sub_plans = subscriberDetails['data_balance']
                if sub_plans:
                    print '%s: Plans - %s' % (subscriberno,
                                              str(sub_plans))
                    renew_status, renew_info = 'No', 'False'
                    try:
                        '''
                        sub_plans['auto_renewal'] = 0
                        if sub_plans['auto_renewal'] == 1:
                            renew_details = sub_plans['renewal_details']
                            renew_name = renew_details['package_name']
                            renew_time = renew_details['renew_at']
                            renew_status = 'Yes : %s at %s' % (renew_name,
                                                               renew_time)
                        '''
                        balances = sub_plans
                        for plan  in balances:
                            sub_plan = balances[plan]
                            print plan, sub_plan
                            raw_amount = int(sub_plan['amount'])
                            if raw_amount > 0:
                                amount = raw_amount/(1024 * 1024)
                            p = {'serviceplan': plan,
                                 'active': 'Yes',
                                 'subdate': sub_plan['purchase_date'][:10],
                                 'expirydate': sub_plan['expiry'],
                                 'fee': sub_plan['price'],
                                 'package': sub_plan['name'],
                                 'auto_renewal': renew_status,
                                 'balance': '%s MB' % (amount)}
                            result_list.append(p)
                    except Exception, e:
                        print 'Failed to get subscriber type %s' % (str(e),)
                        raise e
                if sub_type == "Prepaid":
                    balance = str(balance).strip()
                    response_data = {'prepaid': sub_type, 'balance': balance,
                                     'msg': 'Details for %s found' % (msisdn),
                                     'subscriberno': msisdn,
                                     'serviceplans': result_list}
                else:
                    result_list = []
                    p = {'serviceplan': '-', 'active': 'Yes',
                         'subdate': '-', 'expirydate': '-',
                         'fee': '-', 'package': '-',
                         'balance': '-', 'auto_renewal': '-'}
                    result_list.append(p)
                    response_data = {'prepaid': '-', 'balance': '-',
                                     'msg': 'Details %s NOT found.' % (msisdn),
                                     'subscriberno': msisdn,
                                     'serviceplans': result_list}
                if len(result_list) == 0:
                    p = {'serviceplan': 'PAYG', 'active': 'Yes',
                         'subdate': '-', 'expirydate': '-',
                         'fee': '-', 'package': 'PAY AS YOU GO',
                         'balance': '-', 'auto_renewal': '-'}
                    result_list.append(p)
            else:
                print 'Good'
            return HttpResponse(json.dumps(response_data),
                                mimetype='application/json')
        else:
            form = FrmThreeG()
        return render_to_response('3g.html', {'form': form, 'msg': msg,
                                              'menuselected': '1',
                                              'user_full_names': user_full_names},
                                  context_instance=RequestContext(request))
    except Exception, e:
        msg = 'An error occured while processing your request - %s' % (str(e))
        print msg
        logging.debug(msg)
        return ServerError(msg)


def process_url(params, action):
    import urllib
    import httplib
    from urllib2 import Request, urlopen
    from common.config import application
    params['channel'] = 'gui'
    host = application[action]['ip']
    port = application[action]['port']
    args = urllib.urlencode(params)
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
    returneddetails = ['PAYG,-,-,-,-,PAY AS YOU GO,-,']
    try:
        httplib.HTTPConnection.debuglevel = 1
        conn = httplib.HTTPConnection(host, port)
        print "get_subscriber_packages HOST: %s; PORT: %s" % (host, port)
        conn.request("POST", '/process', args, headers)
        print "get_subscriber_packages POST: %s | %s | %s" \
            % ('/process', args, headers)
        response = conn.getresponse()
        #print 'newton', response.status, response.read()
    except Exception, e:
        print 'Error http read - %s' % (str(e))
        raise e
    else:
        return response


def Balance(msisdn):
    '''
    balance check method
    '''
    params = {'msisdn': msisdn, 'action': 'submitbalance',
              'auto_renewal': 'False', 'packageId': '0'}
    response = process_url(params, 'balance')
    #trans_id = headers['Transaction_id']
    if response.status == 200:
        trans_id = response.read()
    #status_code = headers['Status-Code']
    status, response = get_response(trans_id)
    return response


def provision_package(params, action):
    '''
    balance check method
    '''
    #params['action'] = 'submitprovision'
    response = process_url(params, action)
    status = 3
    if action == 'provision':
        if response.status == 200:
            trans_id = response.read()
        status, resp = get_response(trans_id)
    else:
        resp = response.read()
    return status, resp


def get_response(trans_id, action='balance'):
    my_resp = {}
    params = {'transaction_id': trans_id}
    try:
        status, mytime, count = 0, 30, 0
        while status == 0:
            time.sleep(3)
            count += 3
            if count >= mytime:
                status = 3
            #headers, response = process_url(params, 'response')
            cursor = connection.cursor()
            sql = 'select response from bundle_responses where request_id = '+ trans_id
            print ": Querying database (requests) ... %s" % (sql)
            cursor.execute(sql)
            packagedata = cursor.fetchone()
            if packagedata:
               my_resp = eval(packagedata[0])
               status = my_resp['status']
            if status != 0 and action == 'balance':
                auto_renew = int(my_resp['args']['can_renew'])
                my_resp['active'] = 'Yes'
                my_resp['package_name'] = 'PAYG'
                my_resp['auto_renewal'] = auto_renew
                renew_details = 'False'
                if auto_renew == 1:
                   renew_details = {}
                   renew_details['package_name'] = ''
                   renew_details['renew_at'] = ''
                my_resp['renewal_details'] = renew_details
            elif status != 0 and action != 'balance':
                my_resp['msg'] = response
        print 'Response: request id - %s %s' % (str(trans_id), my_resp)
    except Exception, e:
        print 'Error getting response -%s' % (str(e))
        return 3, my_resp
    else:
        return status, my_resp


@csrf_protect
def provision(request):
    '''
    method to provision request
    '''
    try:
        if (request.method == 'POST'):
            #print request.POST
            subscriberno = str(request.POST.get('msisdn'))
            package_id = str(request.POST.get('packageID'))
            action = str(request.POST.get('action'))
            auto_renew = str(request.POST.get('auto'))
            package = str(request.POST.get('package'))
            opco_code = opco['code']
            m_len = opco['mlen']
            msisdn = opco_code + str(subscriberno)[-m_len:]
            package_name, price = package.split(' - MGA')
            #/provision:  ['msisdn', 'channel', 'package_id',
            #'renew', 'transaction_type' , 'b_msisdn*', 'auth_key']
            #/stop: [channel, msisdn, auth_key]
            if action == 'stop':
                params = {'msisdn': msisdn,
                          'action': 'stop',
                          'packageId': package_id,
                          'auto_renewal': auto_renew}
            else:
                action = 'provision'
                params = {'msisdn': msisdn,
                          'action': 'submitprovision',
                          'packageId': package_id,
                          'auto_renewal': auto_renew,
                          'transaction_type': 'A'}
            print params
            status, response = provision_package(params, action)
            msg = 'Error'
            if action == 'provision':
                #status = int(response['status'])
                if status != 3:
                    balances = response['balance']
                    msg = responses[int(status)]
                vol = ''
                if int(status) == 5:
                    for balance in balances:
                        bundle = balances[balance]
                        bal = int(bundle['amount']) / (1024 * 1024)
                        vol += ', Volume: %sMB, Expiry: %s' % (bal, bundle['expiry'])
                message = 'Status: %s%s' % (msg, vol)
            else:
                resp = eval(response)
                status = int(resp['status'])
                msg = responses[status]
                message = 'Operation completed, Status: %s' % (msg)
            aparams = {}
            aparams['msisdn'] = msisdn
            aparams['service'] = 'Data'
            aparams['package'] = '%s-%s' % (package_name, msg)
            aparams['price'] = int(price.strip())
            aparams['username'] = request.user.get_full_name()
            perform_audit_trail(aparams)
            return HttpResponse(message, mimetype='application/text')
    except Exception, e:
        msg = 'An error occured while processing your request - %s' % (str(e))
        print msg
        logging.debug(msg)
        return ServerError(msg)


#@login_required
def history3g(request, msisdn):
    try:
        opco_code = opco['code']
        m_len = opco['mlen']
        msisdn = opco_code + str(msisdn)[-m_len:]
        sql = '''SELECT a.ID, a.MSISDN, a.COMPLETED_AT, a.REQUEST_ID,
                 b.PACKAGE_NAME, b.PACKAGE_COST, a.CHANNEL from REQUESTS a,
                 new_packages b WHERE b.ID = a.PACKAGE_ID AND a.MSISDN = %s
                 AND a.STATUS = 5 AND rownum <= 50 AND
                 a.PACKAGE_ID != 0 ORDER BY a.CREATED_AT DESC
              ''' % msisdn
        return historyview(request, msisdn, sql)
    except Exception, e:
        msg = 'An error occured while processing your request - %s' % (str(e))
        logging.debug(msg)
        return ServerError(msg)


def historyrenew(request, msisdn):
    try:
        opco_code = opco['code']
        m_len = opco['mlen']
        msisdn = opco_code + str(msisdn)[-m_len:]
        sql = '''SELECT a.ID, a.MSISDN, a.CREATED_AT, a.REQUEST_ID,
                 b.PACKAGE_NAME, b.PACKAGE_COST, a.CHANNEL
                 FROM REQUESTS a, new_packages b WHERE b.ID = a.PACKAGE_ID
                 AND a.MSISDN = '%s' AND a.STATUS = 5 AND a.CHANNEL = 'renewals' AND
                 a.PACKAGE_ID != 0 AND rownum <= 50 ORDER BY a.COMPLETED_AT
              ''' % msisdn
        return historyview(request, msisdn, sql)
    except Exception, e:
        msg = 'An error occured while processing your request - %s' % (str(e))
        logging.debug(msg)
        return ServerError(msg)


def historyview(request, msisdn, sql):
    try:
        if 'user_name' not in request.session:
            msg = 'Session expired. Log in again'
            return render_to_response('expired.html', {'subscriber': msisdn,
                                                       'msg': msg})
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(sql)
        result_list = []
        for row in cursor.fetchall():
            theprice = float(row[5])
            r = {'packagename': row[4], 'price': theprice,
                 'createddatetime': row[2], }
            result_list.append(r)
        cursor.close()
        return render_to_response('3ghistory.html', {'subscriber': msisdn,
                                                     'results': result_list})
    except Exception, e:
        msg = 'An error occured while processing your request - %s' % (str(e))
        logging.debug(msg)
        return ServerError(msg)

def export_history(request, msisdn):
    try:
        opco_code = opco['code']
        m_len = opco['mlen']
        from django.db import connection
        cursor = connection.cursor()
        msisdn = opco_code + str(msisdn)[-m_len:]
        sql = '''SELECT a.ID, a.MSISDN, a.COMPLETED_AT,
                 a.REQUEST_ID, b.PACKAGE_NAME, b.PACKAGE_COST,
                 a.CHANNEL from REQUESTS a, new_packages b where
                 b.ID = a.PACKAGE_ID AND a.MSISDN = %s AND a.STATUS = 5 AND
                 a.PACKAGE_ID != 0 ORDER BY a.COMPLETED_AT DESC
              ''' % msisdn
        cursor.execute(sql)
        response = HttpResponse(mimetype='text/csv')
        f_name = 'attachment;filename=export_3g_%s.csv' % msisdn
        response['Content-Disposition'] = f_name
        writer = csv.writer(response, delimiter=',')
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(cursor)
        cursor.close()
        return response
    except Exception, e:
        msg = 'An error occured while processing your request -%s.' % (str(e))
        logging.debug(msg)
        return ServerError(msg)
