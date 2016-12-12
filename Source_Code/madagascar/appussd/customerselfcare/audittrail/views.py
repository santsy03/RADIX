import csv
import json
from datetime import datetime
from django.db.models import Q
from audittrail.models import Audittrail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.core import ServerError


def perform_audit_trail(params):
    '''
    Method to record all transactions by CC agents
    '''
    try:
        username = params['username']
        msisdn = params['msisdn']
        servicename = params['service']
        packagename = params['package']
        price = params['price']
        add_audittrail = Audittrail(username=username, msisdn=msisdn,
                                    servicename=servicename, price=price,
                                    packagename=packagename,
                                    createddatetime=datetime.now())
        add_audittrail.save()
        params = '%s,%s,%s,%s,%s' % (username, msisdn, servicename,
                                     packagename, price)
        print 'Audit trail saved to Database: %s' % (params)
    except Exception, e:
        print "PerformAuditTrail: Audit trail failed: %s" % (e)


@login_required
def audit_trail(request):
    try:
        if not request.user.is_staff:
            return HttpResponseRedirect('/3g/')
        print "AuditTrail: Querying database (audittrail) ..."
        audits = Audittrail.objects.values('username', 'msisdn',
                                           'servicename', 'packagename',
                                           'price', 'createddatetime'
                                           ).order_by("-createddatetime")[:25]
        p, result_list = {}, []
        for row in audits:
            p = {'username': row['username'], 'msisdn': row['msisdn'],
                 'servicename': row['servicename'], 'price': row['price'],
                 'packagename': row['packagename'],
                 'createddatetime': row['createddatetime'], }
            result_list.append(p)
        if (request.method == 'POST'):
            dfrom = str(request.POST.get('from'))
            dto = str(request.POST.get('to'))
            s_item = str(request.POST.get('text'))
            get_req = request.GET.get
            if get_req('from') and get_req('to') and get_req('text'):
                dfrom = request.GET.get('from')
                dto = request.GET.get('to')
                s_item = request.GET.get('text')
            #response_data = me2udata( subscriberno )
            start_dt = datetime.strptime(dfrom, '%d-%m-%Y')
            start_date = start_dt.strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.strptime(dto, '%d-%m-%Y')
            end_date = end_dt.strftime('%Y-%m-%d %H:%M:%S')
            if s_item:
                avals = Audittrail.objects.values
                a_trails = avals('username', 'msisdn', 'servicename',
                                 'packagename', 'price', 'createddatetime'
                                 ).filter(Q(username__icontains=s_item) |
                                          Q(servicename__icontains=s_item) |
                                          Q(username__icontains=s_item) |
                                          Q(msisdn__icontains=s_item) |
                                          Q(packagename__icontains=s_item) |
                                          Q(price__icontains=s_item) |
                                          Q(createddatetime__icontains=s_item),
                                          Q(createddatetime__range=(start_date,
                                                                    end_date))
                                          ).order_by("-createddatetime")
            else:
                avals = Audittrail.objects.values
                a_trails = avals('username', 'msisdn', 'servicename',
                                 'packagename', 'price', 'createddatetime'
                                 ).filter(Q(createddatetime__range=(start_date,
                                                                    end_date))
                                          ).order_by("-createddatetime")
            ps, response_data = {}, []
            for row in a_trails:
                ps = {'username': row['username'], 'msisdn': row['msisdn'],
                      'servicename': row['servicename'], 'price': row['price'],
                      'packagename': row['packagename'],
                      'createddatetime': (str(row['createddatetime']))[:19]}
                response_data.append(ps)
            return HttpResponse(json.dumps(response_data),
                                mimetype='application/json')
        return render_to_response('audittrail.html', {'results': result_list},
                                  context_instance=RequestContext(request))
    except Exception, e:
        msg = 'AuditTrail: Error while processing your request - %s' % (str(e))
        return ServerError(msg)


@login_required
def export_audit(request):
    try:
        if request.GET.get('from') and request.GET.get('to'):
            dfrom = request.GET.get('from')
            dto = request.GET.get('to')
            start_dt = datetime.strptime(dfrom, '%d-%m-%Y')
            start_date = start_dt.strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.strptime(dto, '%d-%m-%Y')
            end_date = end_dt.strftime('%Y-%m-%d %H:%M:%S')
            avals = Audittrail.objects.values
            if request.GET.get('text'):
                s_item = request.GET.get('text')
                qname = '%s_%s_%s' % (dfrom, dto, s_item.replace(' ', '-'))
                a_trails = avals('username', 'msisdn', 'servicename',
                                 'packagename', 'price', 'createddatetime'
                                 ).filter(Q(username__icontains=s_item) |
                                          Q(servicename__icontains=s_item) |
                                          Q(username__icontains=s_item) |
                                          Q(msisdn__icontains=s_item) |
                                          Q(packagename__icontains=s_item) |
                                          Q(price__icontains=s_item) |
                                          Q(createddatetime__icontains=s_item),
                                          Q(createddatetime__range=(start_date,
                                                                    end_date))
                                          ).order_by("-createddatetime")
            else:
                qname = '%s_%s' % (dfrom, dto)
                a_trails = avals('username', 'msisdn', 'servicename',
                                 'packagename', 'price', 'createddatetime'
                                 ).filter(Q(createddatetime__range=(start_date,
                                                                    end_date))
                                          ).order_by("-createddatetime")
            response = HttpResponse(mimetype='text/csv')
            fname = 'attachment;filename=export_audit_trail_%s.csv' % qname
            response['Content-Disposition'] = fname
            writer = csv.writer(response, delimiter=',')
            writer.writerow(['MSISDN', 'Amount', 'Service', 'Details',
                             'Date / Time', 'CC Agent'])
            for row in a_trails:
                writer.writerow([row['msisdn'], row['price'],
                                row['servicename'], row['packagename'],
                                str(row['createddatetime']),
                                row['username'].encode('utf-8').strip()])
            return response
    except Exception, e:
        msg = 'An error occured while processing your request -%s.' % (str(e))
        return ServerError(msg)
