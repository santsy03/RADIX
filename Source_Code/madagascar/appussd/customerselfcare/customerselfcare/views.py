import logging
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, get_object_or_404
from forms import FrmIndex, FrmThreeG, FrmUploadUsers
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from axes.decorators import watch_login

def ServerError(msg):
    return render_to_response('500.html', {'msg': msg})

@csrf_protect
@watch_login
def home(request):
    try:
        if request.method == 'POST':
            form = FrmIndex(request.POST)
            if form.is_valid():
                user_name = form.data['username']
                pass_word = form.data['password']
                user = authenticate(username=user_name, password=pass_word)
                if user is not None:
                    next_page = '/3g/'
                    meta_vars = request.META
                    ip = meta_vars.get('REMOTE_ADDR')
                    reffer = meta_vars['HTTP_REFERER']
                    if '?next=' in reffer:
                        junk, next_page = reffer.split('?next=')
                    print 'Log in : %s-%s' % (user.username, ip)
                    if user.is_active:
                        login(request, user)
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.username
                        request.session['user_full_names'] = user.first_name + ' ' + user.last_name
                        request.session['user_is_staff'] = user.is_staff
                        #request.session['user_group'] = user.groups.all()
                        return HttpResponseRedirect(next_page)
                    else:
                        msg = "Login Account for username (" + str(user_name) + ") is currently disabled."
                        form = FrmIndex()
                        return render_to_response("index.html", {"form": form, "msg": msg})
                else:
                    msg = "Incorrect username or password."
                    form = FrmIndex()
                    return render_to_response('index.html', {"form": form, "msg": msg})
        else:
            if 'user_id' in request.session:
                del request.session['user_id']
            if 'user_name' in request.session:
                del request.session['user_name']
            if 'user_full_names' in request.session:
                del request.session['user_full_names']
            if 'user_is_staff' in request.session:
                del request.session['user_is_staff']
            if 'user_group' in request.session:
                del request.session['user_group']
            form = FrmIndex()
        return render_to_response('index.html', {"form" : form }, context_instance=RequestContext(request))
    except Exception,e:
        msg = 'An error occured while processing your request. [' + str(e) + ']'
        print str(e)
        logging.debug(msg)
        return ServerError(msg)

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

