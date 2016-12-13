import csv, logging
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from common.config import opco, ME2U_CODES
from common.core import ServerError

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
        response['Content-Disposition'] = 'attachment;filename=export_me2u_%s.csv' % msisdn
        writer = csv.writer(response, delimiter=',')
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(cursor)
        cursor.close()
        return response
    except Exception, e:
        msg = 'An error occured while processing your request. [' + str(e) + ']'
        logging.debug(msg)
        return ServerError(msg)

@login_required
@csrf_protect
def me2u(request):
    if 'user_name' not in request.session:
        return HttpResponseRedirect("/")
    fullname = request.session['user_full_names']
    try:
        if (request.method == 'POST'):
            subscriberno = str(request.POST.get('msisdn'))
            response_data = me2udata( subscriberno )
            #print response_data
            return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
        return render_to_response('me2u.html',{'user_full_names' : fullname, 'menuselected': '2'},
                                  RequestContext(request))
    except Exception, e:
        msg = 'An error occured while processing your request. [' + str(e) + ']'
        print msg
        logging.debug(msg)
        return ServerError(msg)

def me2udata( msisdn ):
    from django.db import connection
    try:
        result_list = []
        if msisdn:
            opco_code = opco['code']
            m_len = opco['mlen']
            cursor = connection.cursor()
            msisdn = opco_code + str(msisdn)[-m_len:]
            sql = '''select recipient, amount, status_code, created_at 
                     from me2u_cdr where msisdn = %s and rownum <= 50
                     order by created_at desc
                  ''' % msisdn
            print sql
            cursor.execute(sql)
            for row in cursor.fetchall():
                status_code = str(row[2])
                #status = ME2U_CODES[status_code]
                res = {'recipient': row[0], 'amount': row[1], 'status': status_code,
                       'created_at': str(row[3]), }
                result_list.append(res)
            cursor.close()
        return result_list
    except Exception, e:
        msg = 'An error occured while processing your request. [' + str(e) + ']'
        print msg
        logging.debug(msg)
        return ServerError(msg)
