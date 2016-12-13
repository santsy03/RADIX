import csv
import urllib
import httplib
import logging
import json
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.config import opco, ME2U_CODES, AUTH_API, STATUS
from common.core import ServerError
from whitelist.views import get_whitelist
from whitelist.forms import FormWhitelist
from audittrail.views import perform_audit_trail
from me2u.models import Users


def get_status(msisdn):
    mylists = Users.objects.filter(username=msisdn)
    return mylists


def pin_status(msisdn):
    plist = get_status(msisdn)
    status, pstatus = 0, 'Not used'
    if plist:
        attempts = plist[0].attempts
        if attempts == 4:
            status = 2
            pstatus = 'Locked'
        else:
            status = 1
            pstatus = 'OK'
    return status, pstatus


def verify_details(params, action):
    '''
    Method for execute PIN actions authenticate/reset/unlock
    '''
    try:
        status_code = 3
        msg = 'Undefined'
        host = AUTH_API['ip']
        port = AUTH_API['port']
        args = urllib.urlencode(params)
        httplib.HTTPConnection.debuglevel = 1
        conn = httplib.HTTPConnection(host, port)
        print "PIN - %s HOST: %s; PORT: %s" % (action, host, port)
        conn.request("GET", '/%s?%s' % (action, args))
        response = conn.getresponse()
        if response.status == 200:
            status_code = int(response.read())
            if status_code in STATUS:
                msg = STATUS[status_code]
    except Exception, e:
        msg = 'An error occured while processing your request -%s.' % (str(e))
        print msg
        logging.debug(msg)
        return 3, 'Error'
    else:
        return status_code, msg


def export_me2u(request, msisdn):
    try:
        opco_code = opco['code']
        m_len = opco['mlen']
        from django.db import connection
        cursor = connection.cursor()
        msisdn = opco_code + str(msisdn)[-m_len:]
        sql = '''select recipient, amount, status_code, created_at
                 from me2u_cdr where msisdn = %s
                 order by created_at desc
              ''' % msisdn
        cursor.execute(sql)
        response = HttpResponse(mimetype='text/csv')
        f_name = 'attachment;filename=export_me2u_%s.csv' % msisdn
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


@login_required
@csrf_protect
def me2u(request):
    if 'user_name' not in request.session:
        return HttpResponseRedirect("/")
    fullname = request.session['user_full_names']
    try:
        package_name, msg = 'PIN', 'Error'
        if (request.method == 'POST'):
            print request.POST
            subscriberno = str(request.POST.get('msisdn'))
            action = int(request.POST.get('action'))
            opco_code = opco['code']
            m_len = opco['mlen']
            msisdn = opco_code + str(subscriberno)[-m_len:]
            params = {}
            params['username'] = msisdn
            params['channel'] = 'gui_%s' % (request.user.username)
            if action == 1:
                response_data = {'code': 9, 'date': 'N/A', 'pin': 0,
                                 'active': 'No', 'pin_status': 'N/A'}
                wlist = get_whitelist(msisdn)
                if wlist:
                    code = wlist[0].active
                    pin, pstatus = pin_status(msisdn)
                    response_data = {'code': code, 'pin': pin,
                                     'active': 'Yes', 'pin_status': pstatus,
                                     'date': str(wlist[0].created_at)}
            elif action == 2:
                response_data = me2udata(msisdn)
            elif action == 3:
                package_name = 'PIN unlock'
                status, msg = verify_details(params, 'unlock')
                response_data = {'code': 0, 'message': msg}
            elif action == 4:
                package_name = 'PIN reset'
                status, msg = verify_details(params, 'reset')
                response_data = {'code': 0, 'message': msg}
            else:
                response_data = {'code': 0, 'message': 'Unknown request'}
            #Fetch last transaction
            if action == 1:
                resp_data = me2udata(msisdn, 1)
                response_data['last_trans'] = resp_data
            if action == 3 or action == 4:
                print 'Audit trail'
                aparams = {}
                aparams['msisdn'] = msisdn
                aparams['service'] = 'Me2u'
                aparams['package'] = '%s-%s' % (package_name, msg)
                aparams['price'] = 0
                aparams['username'] = request.user.get_full_name() 
                perform_audit_trail(aparams)
            return HttpResponse(json.dumps(response_data),
                                mimetype='application/json')
        form = FormWhitelist()
        return render_to_response('me2u.html', {'user_full_names': fullname,
                                                'form': form,
                                                'menuselected': '2'},
                                  RequestContext(request))
    except Exception, e:
        msg = 'An error occured while processing your request -%s.' % (str(e))
        print msg
        logging.debug(msg)
        return ServerError(msg)


def me2udata(msisdn, vals=0):
    from django.db import connection
    try:
        result_list = []
        if msisdn:
            cursor = connection.cursor()
            sql = '''select recipient, amount, status_code, created_at
                     from me2u_cdr where msisdn = %s
                     order by created_at desc
                  ''' % msisdn
            if vals == 1:
                sql = '''select recipient, amount, status_code, created_at
                         from me2u_cdr where msisdn = %s and id = (select
                         max(id) from me2u_cdr where msisdn = %s)
                      ''' % (msisdn, msisdn)
            cursor.execute(sql)
            for row in cursor.fetchall():
                status_code = str(row[2])
                if status_code in ME2U_CODES:
                    status = ME2U_CODES[status_code]
                else:
                    status = status_code
                res = {'recipient': row[0], 'amount': row[1],
                       'status': status,
                       'created_at': str(row[3]), }
                result_list.append(res)
            cursor.close()
        return result_list
    except Exception, e:
        msg = 'An error occured while processing your request -%s.' % (str(e))
        print msg
        logging.debug(msg)
        return ServerError(msg)
