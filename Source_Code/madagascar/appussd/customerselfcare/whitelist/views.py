import csv
import os
import logging
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.core import ServerError
from whitelist.forms import FormWhitelist
from whitelist.models import Whitelist, DealerWhitelist
from audittrail.views import perform_audit_trail
from common.config import opco


def get_whitelist(msisdn, wtype=1):
    #return Whitelist.objects.get('status' >= 0)
    mylists = Whitelist.objects.filter(msisdn=msisdn)
    return mylists


def save_whitelist(msisdn, user_id, wtype=1):
    date_now = datetime.now()
    status = True
    try:
        if wtype == 2:
            mylists = DealerWhitelist(msisdn=msisdn, active=1, created_at=date_now,
                                  modified_at=date_now)
        else:
            mylists = Whitelist(msisdn=msisdn, active=1, created_at=date_now,
                            modified_at=date_now)
        mylists.save()
    except Exception, e:
        print 'Error - %s' % (str(e))
        pass
    else:
        return status


@login_required
def whitelist(request):
    fname = request.session['user_full_names']
    try:
        form = FormWhitelist()
        return render_to_response('whitelist.html', {'form': form,
                                                     'user_full_names': fname},
                                  RequestContext(request))
    except Exception, e:
        msg = 'An error occured while processing your request. [%s]' % (str(e))
        print msg
        logging.debug(msg)
        return ServerError(msg)


@csrf_protect
def process_list(request):
    """
    Retrieve all whitelist details
    """
    if 'user_name' not in request.session:
        msg = 'Session expired. Log in again'
        return render_to_response('expired.html',
                                  {'subscriber': '', 'msg': msg})
    try:
        resp = 'Error processing request'
        if (request.method == 'POST'):
            subscriberno = str(request.POST.get('msisdn'))
            action = int(request.POST.get('action'))
            opco_code = opco['code']
            m_len = opco['mlen']
            msisdn = opco_code + str(subscriberno)[-m_len:]
            wlist = get_whitelist(msisdn, action)
            status = 0
            if action == 1:
                if wlist:
                    code = wlist[0].active
                    if code == 1:
                        status = 1
                        prov_date = wlist[0].modified_at
                        resp = "%s already whitelisted - %s" % (msisdn,
                                                                str(prov_date))
                    else:
                        status = 2
                        create_date = wlist[0].created_at
                        resp = ("%s whitelisted on %s"
                                % (msisdn, str(create_date)))
                else:
                    resp = '%s not whitelisted' % (msisdn)
            elif action == 2:
                if wlist:
                    status = 3
                    resp = "%s already whitelisted" % (msisdn)
                else:
                    status = 4
                    current_user = request.user
                    user_id = current_user.id
                    save_whitelist(msisdn, user_id)
                    resp = "%s successfully whitelisted." % (msisdn)
            params = {}
            params['msisdn'] = msisdn
            params['service'] = 'Me2u'
            params['package'] = (resp.replace(msisdn, '')).strip()
            params['price'] = 0
            params['username'] = request.user.get_full_name()
            perform_audit_trail(params)
            message = {'status': status, 'message': resp}
        return HttpResponse(json.dumps(message),
                            mimetype='application/json; charset=utf8')
    except Exception, e:
        msg = 'An error occured while processing whitelist. [%s]' % (str(e))
        print msg
        logging.debug(msg)
        message = {'status': status, 'message': msg}
        return HttpResponse(json.dumps(message),
                            mimetype='application/json; charset=utf8')


def handle_uploaded_file(request):
    import time
    uname = int(time.time())
    user_name = request.user
    f = request.FILES['msisdns']
    fname = '/appussd/customerselfcare/uploads/%s_%s.txt' % (user_name, uname)
    with open(fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return fname, uname


@csrf_protect
def process_bulk(request):
    '''
    Method to do bulk whitelist from uploaded file
    '''
    try:
        wlist_type = '_whitelist_report.csv'
        msg, status, resp = False, 'Duplicate', False
        cmsisdn, bmsisdn = [], []
        current_user = request.user
        user_id = current_user.id
        if request.is_ajax() and request.method == 'POST':
            actions = int(request.POST.get('actions'))
            if not request.FILES:
                resp_data = {'message': 'No file uploaded'}
            elif actions == 0:
                resp_data = {'message': 'Please select action.'}
            else:
                my_file, uname = handle_uploaded_file(request)
                with open(my_file, 'r') as file_contents:
                    reader = csv.reader(file_contents)
                    try:
                        for row in reader:
                            if len(row) > 0:
                                my_num = row[0].strip()
                                if my_num.isdigit() and len(my_num) >= 9:
                                    cmsisdn.append(my_num)
                                else:
                                    bmsisdn.append(my_num)
                    except csv.Error as e:
                        msg = 'Kindly provide text or csv file - %s' % (str(e))
                if len(cmsisdn) == 0:
                    msg = 'No valid MSISDN in file or empty/invalid file'
                    os.remove(my_file)
                elif len(cmsisdn) > 10000:
                    msg = 'Exceeded max allowed of 10,000'
                if msg:
                    resp_data = {'message': msg}
                else:
                    create_date = datetime.now()
                    rep_file = my_file.replace('.txt', wlist_type)
                    s_count = 0
                    with open(rep_file, 'wb') as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',',
                                                quotechar='"',
                                                quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow(['MSISDN', 'DATE', 'STATUS'])
                        for msisdn in cmsisdn:
                            if actions == 1 or actions == 2:
                                resp = save_whitelist(msisdn, user_id, actions)
                            if resp:
                                s_count += 1
                                status = 'Success'
                            filewriter.writerow([msisdn, create_date, status])
                        for b_msisdn in bmsisdn:
                            filewriter.writerow([b_msisdn, 'Rejected'])
                    s_totals = len(cmsisdn)
                    b_count = s_totals - s_count
                    stats = 'Total %s, Success %s, Duplicates %s' % (s_totals,
                                                                     s_count,
                                                                     b_count)
                    message = ('%s <a href="/whitelist/export/%s">Download Report'
                               '</a>') % (stats, uname)
                    resp_data = {'message': message}
            return HttpResponse(json.dumps(resp_data),
                                mimetype='application/json')
    except Exception, e:
        msg = 'An error occured while processing your request. [%s]' % (str(e))
        print msg
        resp_data = {'message': msg}
        return HttpResponse(json.dumps(resp_data),
                            mimetype='application/json')


@login_required
def export_report(request, report):
    wreport = '%s_whitelist' % (report)
    return export_reports(request, wreport, 2)


@login_required
def export_reports(request, report, rtype = 0):
    try:
        f_name = '%s_%s_report.csv' % (request.user, report)
        r_name = '/appussd/customerselfcare/uploads/%s' % (f_name)
        response = HttpResponse(mimetype='text/csv')
        filename = 'attachment;filename=%s' % (f_name)
        response['Content-Disposition'] = filename
        writer = csv.writer(response, delimiter=',')
        with open(r_name, 'r') as file_contents:
            reader = csv.reader(file_contents)
            if rtype == 0:
                writer.writerow(['MSISDN','STATUS'])
            for row in reader:
                writer.writerow(row)
        return response
    except Exception, e:
        msg = 'An error occured while processing your request. [%s]' % (str(e))
        return ServerError(msg)

