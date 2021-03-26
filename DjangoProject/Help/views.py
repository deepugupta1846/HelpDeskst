from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from datetime import datetime
from datetime import date
import random
from django.core.mail import send_mail
# Create your views here.

def home(request):
    if request.session.get('name', 'none') == 'none':
        return redirect('/login/')
    if request.session.get('user_type') == 'Admin':
        return redirect('/adminpage/')
    elif request.session.get('user_type') == 'Business team':
        return redirect('/business/')
    elif request.session.get('user_type') == 'ML':
        return redirect('/mlpage/')
    elif request.session.get('user_type') == 'Quality Check':
        return redirect('/QualityCheck/')
    elif request.session.get('user_type') == 'Tester':
        return redirect('/Tester/')
    else:
        return redirect('/devloper/')


def userpage(request):
    if request.session.get('name', 'none') == 'none':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    msg = ""
    data = request.session['name']
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    ot = TicketModel.objects.filter(status="Open")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    ut = request.session['user_type']
    if request.method == 'POST':
        d = TicketReply()
        d.user_id = request.session.get('id')
        d.ticket_id = request.POST['qid']
        d.reply_msg = request.POST['rply']
        d.reply_date = date.today()
        d.save()
        msg = "Message sent..."
        subject = "Helpdesk Reply"
        email_to = d.ticket.user.email
        mail_body = f"Hello {d.ticket.user.first_name} {d.ticket.user.mid_name} {d.ticket.user.last_name} \n Your question is :-{d.ticket.question}- \n Replied by : {d.user.first_name} {d.user.mid_name} {d.user.last_name} from {d.user.user_type} \n -Ans. :- {d.reply_msg}  "
        html_message = """
        <div style="margin: 0; padding: 0; background: #91b5ec;">
                            <div style=" border-radius: 30px;
                        box-shadow: 3px 3px 3px #b1b1b1,
                                -3px -3px 3px #555;">
                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                    <ul style="text-align: center;">
                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                    </ul>
                </div>
                
                <div style="background-color:#f2f1ed">
                             
        """
        q = f"<p>Hello <b>{d.ticket.user.first_name} {d.ticket.user.mid_name} {d.ticket.user.last_name} </b></p> <h3>Q. {d.ticket.question}</h3><p>Replied by : <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b> from {d.user.user_type} </p><p>Ans. :-</p><p> {d.reply_msg} </p>"
        html_message += ( q + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False,html_message=html_message)
    return render(request, 'userpage.html', {'ut': ut, 'data':data, 'nt':nt, 'ot':ot, 'msg':msg, 'ct':ct})

def MLpage(request):
    if request.session.get('name', 'none') == 'none':
        return redirect('/login/')
    if request.session['user_type'] != 'ML':
        return redirect('/logout/')
    name = request.session.get('name')
    ut = request.session['user_type']
    return render(request, 'ML.html', {'data': name, 'ut': ut})


def Quality_Check(request):
    if request.session.get('name', 'none') == 'none':
        return redirect('/login/')
    if request.session['user_type'] != 'Quality Check':
        return redirect('/logout/')
    name = request.session.get('name')
    ut = request.session['user_type']
    return render(request, 'Quality_Check.html', {'data': name, 'ut': ut})


def Tester(request):
    if request.session.get('name', 'none') == 'none':
        return redirect('/login/')
    if request.session['user_type'] != 'Tester':
        return redirect('/logout/')
    name = request.session.get('name')
    ut = request.session['user_type']
    return render(request, 'Tester.html', {'data': name, 'ut': ut})


def business(request):
    if request.session.get('name', 'none') == 'none':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    msg = ""
    data = request.session['name']
    ot = TicketModel.objects.filter(status="Open")
    name = request.session.get('name')
    ut = request.session['user_type']
    if request.method == 'POST':
        d = TicketReply()
        d.user_id = request.session.get('id')
        d.ticket_id = request.POST['qid']
        d.reply_msg = request.POST['rply']
        d.reply_date = date.today()
        d.save()
        msg = "Message sent..."
        subject = "Helpdesk Reply"
        email_to = d.ticket.user.email
        mail_body = f"Hello {d.ticket.user.first_name} {d.ticket.user.mid_name} {d.ticket.user.last_name} \n Your question is :-{d.ticket.question}- \n Replied by : {d.user.first_name} {d.user.mid_name} {d.user.last_name} from {d.user.user_type} \n -Ans. :- {d.reply_msg}  "
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False)
    replymsg = TicketReply.objects.all()
    return render(request, 'businesspage.html', {'data': data, 'name':name, 'ut':ut, 'ot':ot, 'msg':msg, 'replymsg':replymsg})


def emailinput(request):
    m = ""
    if request.method == 'POST':
        email_id = request.POST['em']
        d = UserModel.objects.filter(email__exact=email_id)
        if len(d) != 0:
            m = "Email already exists!"
            return render(request, 'emailinput.html', { 'm': m})
        password = request.POST['pass']
        rand = random.randint(100000, 999999)
        message = f"your otp is {rand}"
        subject = "HelpDesk Email Verification"
        html_message = """
                                <div style="margin: 0; padding: 0; background: #91b5ec;">
                                                    <div style=" border-radius: 30px;
                                                box-shadow: 3px 3px 3px #b1b1b1,
                                                        -3px -3px 3px #555;">
                                            <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                            <ul style="text-align: center;">
                                                <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                            </ul>
                                        </div>

                                        <div style="background-color:#f2f1ed; padding:10px;">

                                """
        q = f"<h2>Welcome To Tech Assist </h2><p>your otp is {rand}</p>"
        html_message += (q + '</div></div>')
        send_mail(subject, message, 'helpdeskricla@gmail.com', [email_id], fail_silently=False, html_message=html_message)
        request.session['email_id'] = email_id
        request.session['password'] = password
        request.session['otp_msg'] = rand
        return redirect('/otpvalidation/')
    return render(request, 'emailinput.html')


def otpvalidation(request):
    if request.session.get('email_id', 'None') == 'None':
        return redirect('/emailinput/')
    msg = ""
    emails = request.session.get('email_id')
    if request.method == 'POST':
        otp = request.POST['otp']
        email_otp = request.session.get('otp_msg')
        if str(otp) == str(email_otp):
            del request.session['otp_msg']
            request.session['validate_mail'] = request.session.get('email_id')
            return redirect('/signup/')
        else:
            msg = "Incorrect OTP"
    return render(request, 'otpinput.html', {'msg': msg, 'emails':emails})


def signup(request):
    if request.session.get('validate_mail', 'None') == 'None':
        del request.session['email_id']
        return redirect('/emailinput/')
    msg = ""
    emails = request.session.get('email_id')
    passw = request.session.get('password')
    if request.method == 'POST':
        form = UserModel(first_name=request.POST['first_name'], mid_name=request.POST['mid_name'], last_name=request.POST['last_name'], gender=request.POST['gender'], email=emails, user_type=request.POST['user_type'], password=passw)
        form.save()
        msg = "Your request is submited successfully. Please wait for the admin to verify."
        del request.session['email_id']
        subject = "Tech Assist"
        mail_body = "Hello"
        email_to = form.email
        html_message = """
                        <div style="margin: 0; padding: 0; background: #91b5ec;">
                                            <div style=" border-radius: 30px;
                                        box-shadow: 3px 3px 3px #b1b1b1,
                                                -3px -3px 3px #555;">
                                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                    <ul style="text-align: center;">
                                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                    </ul>
                                </div>

                                <div style="background-color:#f2f1ed; padding:10px;">

                        """
        q = f"<h2>Welcome To Tech Assist </h2><p>Hello <b>{form.first_name} {form.mid_name} {form.last_name} </b><br/><p>Your request is submited successfully. Please wait for the admin to verify.</p>"
        html_message += (q + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
        return redirect('/login/')
    form = UserForm()
    return render(request, 'signup.html', {'form':form, 'msg':msg})


def adminPage(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    msg = ""
    data = request.session['name']
    new_request = UserModel.objects.filter(approved_by=None)
    tn = len(new_request)
    ot = TicketModel.objects.filter(status="Open")
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    ut = request.session['user_type']
    if request.method == 'POST':
        d = TicketReply()
        d.user_id = request.session.get('id')
        d.ticket_id = request.POST['qid']
        d.reply_msg = request.POST['rply']
        d.reply_date = date.today()
        d.save()
        msg = "Message sent..."
        subject = "Helpdesk Reply"
        email_to = d.ticket.user.email
        mail_body = f"Hello {d.ticket.user.first_name} {d.ticket.user.mid_name} {d.ticket.user.last_name} \n Your question is :-{d.ticket.question}- \n Replied by : {d.user.first_name} {d.user.mid_name} {d.user.last_name} from {d.user.user_type} \n -Ans. :- {d.reply_msg}  "
        html_message = """
            <div style="margin: 0; padding: 0; background: #91b5ec;">
                                <div style=" border-radius: 30px;
                            box-shadow: 3px 3px 3px #b1b1b1,
                                    -3px -3px 3px #555;">
                        <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                        <ul style="text-align: center;">
                            <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                        </ul>
                    </div>

                    <div style="background-color:#f2f1ed">

            """
        q = f"<p>Hello <b>{d.ticket.user.first_name} {d.ticket.user.mid_name} {d.ticket.user.last_name} </b></p> <h3>Q. {d.ticket.question}</h3><p>Replied by : <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b> from {d.user.user_type} </p><p>Ans. :-</p><p> {d.reply_msg} </p>"
        html_message += (q + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False,
                  html_message=html_message)
    return render(request, 'adminpage.html', {'data': data, 'tn': tn, 'ut': ut, 'msg':msg, 'ot':ot, 'nt':nt, 'ct':ct})




def login(request):
    m = ""
    if request.method == 'POST':
        users = UserModel.objects.filter(email__exact=request.POST['emailid']).filter(password__exact=request.POST['paasword'])
        if len(users) != 0 and users[0].revoked_by == None:
            if users[0].approved_by != None:
                request.session['name'] = users[0].first_name
                request.session['id'] = users[0].id
                request.session['user_type'] = users[0].user_type
                f = LoginHistory()
                f.user_id = users[0].id
                f.login_at = datetime.today()
                f.save()
                request.session['loginid'] = f.id
                if users[0].user_type == 'Admin':
                    return redirect('/adminpage/')
                elif users[0].user_type == 'Business team':
                    return redirect('/business/')
                elif users[0].user_type == 'ML':
                    return redirect('/mlpage/')
                elif users[0].user_type == 'Quality Check':
                    return redirect('/QualityCheck/')
                elif users[0].user_type == 'Tester':
                    return redirect('/Tester/')
                else:
                    return redirect('/devloper/')
            else:
                m = "Currently you cannot login as you request is pending."
        else:
            m = "Invalid User Name And Password!"
    return render(request, 'base.html', {'m': m})


def user_request(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    new_request = UserModel.objects.filter(approved_by=None)
    tn = len(new_request)

    return render(request, 'adminpage.html', {'tn': tn})


def view_all_request(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    new_request = UserModel.objects.filter(approved_by=None)
    tnr = len(new_request)
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    return render(request, 'viewnewrequest.html', {'tr': new_request, 'tnr': tnr, 'data' : data, 'ut': ut, 'nt':nt,'ct':ct})


def view_Approvel(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    new_request = UserModel.objects.filter(approved_by=None)
    tnr = len(new_request)
    all_apr = UserModel.objects.all()
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    return render(request, 'viewallprovel.html', {'all_apr': all_apr, 'data':data, 'ut':ut, 'tn': tnr, 'nt':nt,'ct':ct})


def all_user(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    new_request = UserModel.objects.filter(approved_by=None)
    tnr = len(new_request)
    all_apr = UserModel.objects.all()
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    return render(request, 'alluser.html', {'all_apr': all_apr, 'data':data, 'ut':ut, 'tn': tnr, 'nt':nt,'ct':ct})


def reject(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    d = UserModel.objects.get(id=id)
    d.delete()
    subject = "Tech Assist"
    email_to = d.email
    mail_body = f"Hello {d.first_name} {d.mid_name} {d.last_name} \n Congrats! you are approved by Admin {request.session.get('id')}-{request.session.get('name')} \n Your ID no.: {d.id}\nUser Type.: {d.user_type}\napproved_date: {d.approved_date}\n☺"
    html_message = """
                        <div style="margin: 0; padding: 0; background: #91b5ec;">
                                            <div style=" border-radius: 30px;
                                        box-shadow: 3px 3px 3px #b1b1b1,
                                                -3px -3px 3px #555;">
                                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                    <ul style="text-align: center;">
                                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                    </ul>
                                </div>

                                <div style="background-color:#f2f1ed; padding:10px;">

                        """
    q = f"Hello <b>{d.first_name} {d.mid_name} {d.last_name}</b><p> your request  has been rejected by Admin <b>{request.session.get('id')}-{request.session.get('name')} </b></p><br/><p> Your ID no. - <b>{d.id}</b></p><p> Gmail ID. - <b>{d.email}</b></p><p>Password - <b>{d.password}</b></p><p>User Type - <b>{d.user_type}</b><p>Approved_date: <b>{d.approved_date}</b></p><br/><p>Thanks</p>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    return redirect('/viewnewrequest/')


def accept(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    d = UserModel.objects.get(id=id)
    d.approved_by = request.session.get('id')
    d.approved_date = date.today()
    d.save()
    subject = "Tech Assist"
    email_to = d.email
    mail_body = f"Hello {d.first_name} {d.mid_name} {d.last_name} \n Congrats! you are approved by Admin {request.session.get('id')}-{request.session.get('name')} \n Your ID no.: {d.id}\nUser Type.: {d.user_type}\napproved_date: {d.approved_date}\n☺"
    html_message = """
                    <div style="margin: 0; padding: 0; background: #91b5ec;">
                                        <div style=" border-radius: 30px;
                                    box-shadow: 3px 3px 3px #b1b1b1,
                                            -3px -3px 3px #555;">
                                <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                <ul style="text-align: center;">
                                    <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                </ul>
                            </div>

                            <div style="background-color:#f2f1ed; padding:10px;">

                    """
    q = f"Hello <b>{d.first_name} {d.mid_name} {d.last_name}</b><p> Congrats! you are approved by Admin <b>{request.session.get('id')}-{request.session.get('name')} </b></p><br/><p> Your ID no. - <b>{d.id}</b></p><p> Gmail ID. - <b>{d.email}</b></p><p>Password - <b>{d.password}</b></p><p>User Type - <b>{d.user_type}</b><p>Approved_date: <b>{d.approved_date}</b></p><br/><p>Thanks</p>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    return redirect('/viewnewrequest/')



def revoke(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    d = UserModel.objects.get(id=id)
    d.revoked_by = request.session.get('id')
    d.revoke_date = date.today()
    d.save()
    return redirect('/viewapprovel/')



def allrevokeusers(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    revoke_user = UserModel.objects.all()
    new_request = UserModel.objects.filter(approved_by=None)
    tnr = len(new_request)
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    return render(request, 'allrevokeuser.html', {'revoke_user': revoke_user, 'data':data, 'ut':ut, 'tn': tnr, 'nt':nt,'ct':ct})


def logout(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    e = request.session.get('loginid')
    f = LoginHistory.objects.get(id=e)
    f.logout_on = datetime.today()
    f.save()
    del request.session['name']
    del request.session['loginid']
    return redirect('/login/')


def developerprofile(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    name = request.session.get('name')
    ut = request.session['user_type']
    userdata = UserModel.objects.get(id=request.session['id'])
    return render(request, 'userprofile.html', {'userdata': userdata, 'data': name, 'ut':ut})


def businessprofile(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    name = request.session.get('name')
    ut = request.session['user_type']
    userdata = UserModel.objects.get(id=request.session['id'])
    return render(request, 'businessprofile.html', {'userdata': userdata, 'data': name, 'ut':ut})


def adminprofile(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    userdata = UserModel.objects.get(id=request.session['id'])
    new_request = UserModel.objects.filter(approved_by=None)
    tn = len(new_request)
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    return render(request, 'adminprofile.html', {'userdata': userdata, 'tn': tn, 'nt':nt,'ct':ct})


def logInHistory(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    new_request = UserModel.objects.filter(approved_by=None)
    tnr = len(new_request)
    log = LoginHistory.objects.all()
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    return render(request, 'loginhistory.html', {'logInHistory': log, 'data':data, 'ut':ut, 'tn': tnr,'nt':nt,'ct':ct})


def newticketRaise(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    userid = request.session.get('id')
    msg = ""
    if request.method == 'POST':
        form = TicketModel(user_id=userid, status="New", categrories=request.POST['categrories'], ticket_type=request.POST['ticket_type'], question=request.POST['question'], description=request.POST['description'], ticket_raise_date = datetime.today() )
        form.save()
        msg = "Ticket Raised Successfully......."
        subject = "Tech Assist Ticket"
        email_to = form.user.email
        mail_body = ""
        html_message = """
                        <div style="margin: 0; padding: 0; background: #91b5ec;">
                                            <div style=" border-radius: 30px;
                                        box-shadow: 3px 3px 3px #b1b1b1,
                                                -3px -3px 3px #555;">
                                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                    <ul style="text-align: center;">
                                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                    </ul>
                                </div>

                                <div style="background-color:#f2f1ed; padding:10px;">

                        """
        q = f"<p>Hello <b>{form.user.first_name} {form.user.mid_name} {form.user.last_name} </b></p><p>Your ticket raised successfully </p><p><h3>Q.{form.id} {form.question}</h3></p><p>Description - <b>{form.description}</b><p>Ticket Category - <b>{form.categrories}</b></p><p>Ticket Type - <b>{form.ticket_type}</b></p><p>Raised Date - <b>{form.ticket_raise_date}</b>"
        html_message += (q + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)

        a = UserModel.objects.filter(user_type__exact="Admin")
        d = UserModel.objects.filter(user_type__exact="Developer")
        Developer = []
        for i in d:
            Developer.append(i.email)

        admins = []
        for i in a:
            admins.append(i.email)
        html_message2 = """
                                        <div style="margin: 0; padding: 0; background: #91b5ec;">
                                                            <div style=" border-radius: 30px;
                                                        box-shadow: 3px 3px 3px #b1b1b1,
                                                                -3px -3px 3px #555;">
                                                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                                    <ul style="text-align: center;">
                                                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                                    </ul>
                                                </div>

                                                <div style="background-color:#f2f1ed; padding:10px;">

                                        """
        a = f"<p>A ticket raised by <b><b>{form.user.first_name} {form.user.mid_name} {form.user.last_name}</b> </p><p><h3>Q.{form.id} {form.question}</h3></p><p>Description - <b>{form.description}</b><p>Ticket Category - <b>{form.categrories}</b></p><p>Ticket Type - <b>{form.ticket_type}</b></p><p>Raised Date - <b>{form.ticket_raise_date}</b>"
        html_message2 += (a + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', admins, fail_silently=False,html_message=html_message2)
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', Developer, fail_silently=False,html_message=html_message2)
    form = TicketForm()
    data = request.session['name']
    ut = request.session['user_type']
    return render(request, 'ticketraise.html', {'form':form, 'msg':msg, 'data': data, 'ut':ut})


def showRaiseTicket(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    u = request.session.get('id')
    rt = TicketModel.objects.filter(user=u)
    data = request.session['name']
    ut = request.session['user_type']
    return render(request, 'showraiseticket.html', {'rt': rt, 'data': data, 'ut': ut})

def deleteTicket(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    data = TicketModel.objects.get(id=id)
    data.delete()
    return redirect('/showraiseticket/')


def newRaisedTicket(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    return render(request, 'newraisedticket.html', {'rt': new_Raised_Ticket, 'data':data, 'ut':ut, 'nt':nt,'ct':ct})


def newRaisedTicketinadmin(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    new_request = UserModel.objects.filter(approved_by=None)
    tn = len(new_request)
    return render(request, 'admin_new_raised_ticket.html', {'rt': new_Raised_Ticket, 'data':data, 'ut':ut, 'nt':nt,'ct':ct, 'tn': tn,})


def showclosedTicket(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    return render(request, 'closedticket.html', {'rt': closed_Ticket, 'data':data, 'ut':ut, 'ct':ct, 'nt':nt})


def showclosedTicketinAdmin(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    data = request.session.get('name')
    ut = request.session.get('user_type')
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    ct = len(closed_Ticket)
    new_Raised_Ticket = TicketModel.objects.filter(status="New")
    nt = len(new_Raised_Ticket)
    new_request = UserModel.objects.filter(approved_by=None)
    tn = len(new_request)
    return render(request, 'admin_show_closed_ticket.html', {'rt': closed_Ticket, 'data':data, 'ut':ut, 'ct':ct, 'nt':nt, 'tn': tn,})


def ticketopen(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    d = TicketModel.objects.get(id=id)
    d.status = "Open"
    d.ticket_opened_by = request.session.get('id')
    d.ticket_open_date = date.today()
    d.save()
    f = UserModel.objects.get(id=d.ticket_opened_by)
    subject = "Tech Assist Ticket Status"
    mail_body = ""
    email_to = d.user.email
    html_message = """
        <div style="margin: 0; padding: 0; background: #91b5ec;">
                            <div style=" border-radius: 30px;
                        box-shadow: 3px 3px 3px #b1b1b1,
                                -3px -3px 3px #555;">
                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                    <ul style="text-align: center;">
                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                    </ul>
                </div>

                <div style="background-color:#f2f1ed; padding:10px;">
        """
    q = f"<p>Hello <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name} </b></p><p>Your ticket Opened </p><p><h3>Q.{d.id} {d.question}</h3></p><p>Opened by - <b>{d.ticket_opened_by} {f.first_name} {f.mid_name} {f.last_name} </b><p>Opened Date - <b>{d.ticket_open_date}</b>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    email2 = f.email
    html_message2 = """
            <div style="margin: 0; padding: 0; background: #91b5ec;">
                                <div style=" border-radius: 30px;
                            box-shadow: 3px 3px 3px #b1b1b1,
                                    -3px -3px 3px #555;">
                        <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                        <ul style="text-align: center;">
                            <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                        </ul>
                    </div>

                    <div style="background-color:#f2f1ed; padding:10px;">
            """
    q = f"<p>Hello <b>{f.first_name} {f.mid_name} {f.last_name} </b></p><p>You opened a ticket </p><p><h3>Q.{d.id} {d.question}</h3><p>Raised by - <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b></p><p>Raised Date - <b>{d.ticket_raise_date}</b></p><p>Opened Date - <b>{d.ticket_open_date}</b></p>"
    html_message2 += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email2], fail_silently=False, html_message=html_message2)
    return redirect('/newraisedticket/')

def closedTicketOpen(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    d = TicketModel.objects.get(id=id)
    d.status = "Open"
    d.ticket_opened_by = request.session.get('id')
    d.ticket_open_date = date.today()
    d.save()
    f = UserModel.objects.get(id=d.ticket_opened_by)
    subject = "Tech Assist Ticket Status"
    mail_body = ""
    email_to = d.user.email
    html_message = """
        <div style="margin: 0; padding: 0; background: #91b5ec;">
                            <div style=" border-radius: 30px;
                        box-shadow: 3px 3px 3px #b1b1b1,
                                -3px -3px 3px #555;">
                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                    <ul style="text-align: center;">
                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                    </ul>
                </div>

                <div style="background-color:#f2f1ed; padding:10px;">
        """
    q = f"<p>Hello <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name} </b></p><p>Your ticket Opened </p><p><h3>Q.{d.id} {d.question}</h3></p><p>Opened by - <b>{d.ticket_opened_by} {f.first_name} {f.mid_name} {f.last_name} </b><p>Opened Date - <b>{d.ticket_open_date}</b>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    email2 = f.email
    html_message2 = """
            <div style="margin: 0; padding: 0; background: #91b5ec;">
                                <div style=" border-radius: 30px;
                            box-shadow: 3px 3px 3px #b1b1b1,
                                    -3px -3px 3px #555;">
                        <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                        <ul style="text-align: center;">
                            <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                        </ul>
                    </div>

                    <div style="background-color:#f2f1ed; padding:10px;">
            """
    q = f"<p>Hello <b>{f.first_name} {f.mid_name} {f.last_name} </b></p><p>You opened a ticket </p><p><h3>Q.{d.id} {d.question}</h3><p>Raised by - <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b></p><p>Raised Date - <b>{d.ticket_raise_date}</b></p><p>Opened Date - <b>{d.ticket_open_date}</b></p>"
    html_message2 += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email2], fail_silently=False, html_message=html_message2)
    return redirect('/showclosedticket/')


def ticketopenbyadmin(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    d = TicketModel.objects.get(id=id)
    d.status = "Open"
    d.ticket_opened_by = request.session.get('id')
    d.ticket_open_date = date.today()
    d.save()
    f = UserModel.objects.get(id=d.ticket_opened_by)
    subject = "Tech Assist Ticket Status"
    mail_body = ""
    email_to = d.user.email
    html_message = """
        <div style="margin: 0; padding: 0; background: #91b5ec;">
                            <div style=" border-radius: 30px;
                        box-shadow: 3px 3px 3px #b1b1b1,
                                -3px -3px 3px #555;">
                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                    <ul style="text-align: center;">
                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                    </ul>
                </div>

                <div style="background-color:#f2f1ed; padding:10px;">
        """
    q = f"<p>Hello <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name} </b></p><p>Your ticket Opened </p><p><h3>Q.{d.id} {d.question}</h3></p><p>Opened by - <b>{d.ticket_opened_by} {f.first_name} {f.mid_name} {f.last_name} </b><p>Opened Date - <b>{d.ticket_open_date}</b>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    email2 = f.email
    html_message2 = """
            <div style="margin: 0; padding: 0; background: #91b5ec;">
                                <div style=" border-radius: 30px;
                            box-shadow: 3px 3px 3px #b1b1b1,
                                    -3px -3px 3px #555;">
                        <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                        <ul style="text-align: center;">
                            <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                        </ul>
                    </div>

                    <div style="background-color:#f2f1ed; padding:10px;">
            """
    q = f"<p>Hello <b>{f.first_name} {f.mid_name} {f.last_name} </b></p><p>You opened a ticket </p><p><h3>Q.{d.id} {d.question}</h3><p>Raised by - <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b></p><p>Raised Date - <b>{d.ticket_raise_date}</b></p><p>Opened Date - <b>{d.ticket_open_date}</b></p>"
    html_message2 += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email2], fail_silently=False, html_message=html_message2)
    return redirect('/newraisedticketadmin/')


def ticketopenbyadminafterclosed(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    d = TicketModel.objects.get(id=id)
    d.status = "Open"
    d.ticket_opened_by = request.session.get('id')
    d.ticket_open_date = date.today()
    d.save()
    f = UserModel.objects.get(id=d.ticket_opened_by)
    subject = "Tech Assist Ticket Status"
    mail_body = ""
    email_to = d.user.email
    html_message = """
        <div style="margin: 0; padding: 0; background: #91b5ec;">
                            <div style=" border-radius: 30px;
                        box-shadow: 3px 3px 3px #b1b1b1,
                                -3px -3px 3px #555;">
                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                    <ul style="text-align: center;">
                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                    </ul>
                </div>

                <div style="background-color:#f2f1ed; padding:10px;">
        """
    q = f"<p>Hello <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name} </b></p><p>Your ticket Opened </p><p><h3>Q.{d.id} {d.question}</h3></p><p>Opened by - <b>{d.ticket_opened_by} {f.first_name} {f.mid_name} {f.last_name} </b><p>Opened Date - <b>{d.ticket_open_date}</b>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    email2 = f.email
    html_message2 = """
            <div style="margin: 0; padding: 0; background: #91b5ec;">
                                <div style=" border-radius: 30px;
                            box-shadow: 3px 3px 3px #b1b1b1,
                                    -3px -3px 3px #555;">
                        <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                        <ul style="text-align: center;">
                            <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                        </ul>
                    </div>

                    <div style="background-color:#f2f1ed; padding:10px;">
            """
    q = f"<p>Hello <b>{f.first_name} {f.mid_name} {f.last_name} </b></p><p>You opened a ticket </p><p><h3>Q.{d.id} {d.question}</h3><p>Raised by - <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b></p><p>Raised Date - <b>{d.ticket_raise_date}</b></p><p>Opened Date - <b>{d.ticket_open_date}</b></p>"
    html_message2 += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email2], fail_silently=False, html_message=html_message2)
    return redirect('/showclosedticketadmin/')


def ticketclosed(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    d = TicketModel.objects.get(id=id)
    d.status = "Solved"
    d.ticket_closed_by = request.session.get('id')
    d.ticket_close_date = date.today()
    d.save()
    f = UserModel.objects.get(id=d.ticket_opened_by)
    subject = "Tech Assist Ticket Status"
    mail_body = ""
    email_to = d.user.email
    html_message = """
            <div style="margin: 0; padding: 0; background: #91b5ec;">
                                <div style=" border-radius: 30px;
                            box-shadow: 3px 3px 3px #b1b1b1,
                                    -3px -3px 3px #555;">
                        <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                        <ul style="text-align: center;">
                            <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                        </ul>
                    </div>

                    <div style="background-color:#f2f1ed; padding:10px;">
            """
    q = f"<p>Hello <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name} </b></p><p>Your ticket Closed </p><p><h3>Q.{d.id} {d.question}</h3></p><p>Closed by - <b>{d.ticket_closed_by} {f.first_name} {f.mid_name} {f.last_name} </b><p>Closed Date - <b>{d.ticket_close_date}</b>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    email2 = f.email
    html_message2 = """
                <div style="margin: 0; padding: 0; background: #91b5ec;">
                                    <div style=" border-radius: 30px;
                                box-shadow: 3px 3px 3px #b1b1b1,
                                        -3px -3px 3px #555;">
                            <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                            <ul style="text-align: center;">
                                <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                            </ul>
                        </div>

                        <div style="background-color:#f2f1ed; padding:10px;">
                """
    q = f"<p>Hello <b>{f.first_name} {f.mid_name} {f.last_name} </b></p><p>You closed a ticket </p><p><h3>Q.{d.id} {d.question}</h3><p>Raised by - <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b></p><p>Raised Date - <b>{d.ticket_raise_date}</b></p><p>Closed Date - <b>{d.ticket_close_date}</b></p>"
    html_message2 += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email2], fail_silently=False, html_message=html_message2)
    return redirect('/devloper/')


def ticketclosedbyadmin(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    d = TicketModel.objects.get(id=id)
    d.status = "Solved"
    d.ticket_closed_by = request.session.get('id')
    d.ticket_close_date = date.today()
    d.save()
    f = UserModel.objects.get(id=d.ticket_opened_by)
    subject = "Tech Assist Ticket Status"
    mail_body = ""
    email_to = d.user.email
    html_message = """
            <div style="margin: 0; padding: 0; background: #91b5ec;">
                                <div style=" border-radius: 30px;
                            box-shadow: 3px 3px 3px #b1b1b1,
                                    -3px -3px 3px #555;">
                        <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                        <ul style="text-align: center;">
                            <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                        </ul>
                    </div>

                    <div style="background-color:#f2f1ed; padding:10px;">
            """
    q = f"<p>Hello <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name} </b></p><p>Your ticket Closed </p><p><h3>Q.{d.id} {d.question}</h3></p><p>Closed by - <b>{d.ticket_closed_by} {f.first_name} {f.mid_name} {f.last_name} </b><p>Closed Date - <b>{d.ticket_close_date}</b>"
    html_message += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    email2 = f.email
    html_message2 = """
                <div style="margin: 0; padding: 0; background: #91b5ec;">
                                    <div style=" border-radius: 30px;
                                box-shadow: 3px 3px 3px #b1b1b1,
                                        -3px -3px 3px #555;">
                            <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                            <ul style="text-align: center;">
                                <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                            </ul>
                        </div>

                        <div style="background-color:#f2f1ed; padding:10px;">
                """
    q = f"<p>Hello <b>{f.first_name} {f.mid_name} {f.last_name} </b></p><p>You closed a ticket </p><p><h3>Q.{d.id} {d.question}</h3><p>Raised by - <b>{d.user.first_name} {d.user.mid_name} {d.user.last_name}</b></p><p>Raised Date - <b>{d.ticket_raise_date}</b></p><p>Closed Date - <b>{d.ticket_close_date}</b></p>"
    html_message2 += (q + '</div></div>')
    send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email2], fail_silently=False, html_message=html_message2)
    return redirect('/adminpage/')


def show_replied_msg(request):
    if request.session.get('name', 'none') == 'none':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    msg = ""
    data = request.session['name']
    name = request.session.get('name')
    ut = request.session['user_type']
    u = request.session.get('id')
    replymsg = TicketReply.objects.all()
    if request.method == 'POST':
        d = ReplyToReply()
        d.tReply_id = request.POST['reply_id']
        d.userm_id = request.session['id']
        d.rplymsg = request.POST['rtor']
        d.rplymsgdate = datetime.today()
        d.save()
        msg = "Reply sent...."
        subject = "Tech Assist"
        email_to = d.tReply.user.email
        mail_body = "Hello"
        html_message = """
                <div style="margin: 0; padding: 0; background: #91b5ec;">
                                    <div style=" border-radius: 30px;
                                box-shadow: 3px 3px 3px #b1b1b1,
                                        -3px -3px 3px #555;">
                            <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                            <ul style="text-align: center;">
                                <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                            </ul>
                        </div>

                        <div style="background-color:#f2f1ed; padding:10px;">

                """
        q = f"<p>Hello <b>{d.tReply.user.first_name} {d.tReply.user.mid_name} {d.tReply.user.last_name} </b></p><p>Your message : {d.tReply.reply_msg} </p><p>Comment on<h3>Q.{d.tReply.ticket.id} {d.tReply.ticket.question}</h3></p><br/><br/><p>Replied by: <b>{d.userm.first_name} {d.userm.mid_name} {d.userm.last_name}</b> from <b>{d.userm.user_type}</b></p><p>Replied Message : {d.rplymsg}</p>"
        html_message += (q + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False, html_message=html_message)
    return render(request, 'repliedmsg.html', {'data': data, 'name': name, 'ut': ut, 'replymsg': replymsg, 'uid':u, 'msg':msg})


def showOpenedbyname(request, ticket_opened_by):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    f = UserModel.objects.get(id=ticket_opened_by)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    return render(request, 'admin_ticket_openedby_profile.html', {'userdata':f, 'data':data,'ut':ut})


def showOpenedbynamedeveloper(request, ticket_opened_by):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    f = UserModel.objects.get(id=ticket_opened_by)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    return render(request, 'developer_ticket_openedby_profile.html', {'userdata':f, 'data':data,'ut':ut})


def showOpenedbynamebusiness(request, ticket_opened_by):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    f = UserModel.objects.get(id=ticket_opened_by)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    return render(request, 'business_ticket_openby_profile.html', {'userdata':f, 'data':data,'ut':ut})


def showApprovedby(request, approved_by):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    f = UserModel.objects.get(id=approved_by)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    return render(request, 'admin_ticket_openedby_profile.html', {'userdata':f, 'data':data,'ut':ut})

def showApprovedbyinalluser(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    f = UserModel.objects.get(id=id)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    return render(request, 'show_Approved_by_inalluser.html', {'userdata':f, 'data':data,'ut':ut})


def getTotalNewTicketNumber(request):
    NumberOfTicket = TicketModel.objects.filter(status="New")
    nofticket = len(NumberOfTicket)
    new_request = UserModel.objects.filter(approved_by=None)
    nofnewrequest = len(new_request)
    closed_Ticket = TicketModel.objects.filter(status="Solved")
    nofclosedticket = len(closed_Ticket)
    data = {"nofTicket": nofticket, "nofNewRequest": nofnewrequest,  "nofClosedTicket": nofclosedticket}
    return JsonResponse(data)


def ShowReplyMsgBusiness(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Business team':
        return redirect('/logout/')
    Reply_data = TicketReply.objects.filter(ticket_id=id)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    rid = request.session.get('id')
    msg = ""
    if request.method == 'POST':
        d = ReplyToReply()
        d.tReply_id = request.POST['reply_id']
        d.userm_id = request.session['id']
        d.rplymsg = request.POST['rtor']
        d.rplymsgdate = datetime.today()
        d.save()
    return render(request, 'Business_Ticket_Reply.html', {'Reply_data':Reply_data, 'data':data,'ut':ut, 'msg':msg})


def ShowReplyMsgAdmin(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    rid = request.session.get('id')
    Reply_data = TicketReply.objects.filter(ticket_id=id)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    msg = ""
    if request.method == 'POST':
        d = ReplyToReply()
        d.tReply_id = request.POST['reply_id']
        d.userm_id = request.session['id']
        d.rplymsg = request.POST['rtor']
        d.rplymsgdate = datetime.today()
        d.save()
        msg = "Reply sent...."
        subject = "Tech Assist"
        email_to = d.tReply.user.email
        mail_body = "Hello"
        html_message = """
                        <div style="margin: 0; padding: 0; background: #91b5ec;">
                                            <div style=" border-radius: 30px;
                                        box-shadow: 3px 3px 3px #b1b1b1,
                                                -3px -3px 3px #555;">
                                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                    <ul style="text-align: center;">
                                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                    </ul>
                                </div>

                                <div style="background-color:#f2f1ed; padding:10px;">

                        """
        q = f"<p>Hello <b>{d.tReply.user.first_name} {d.tReply.user.mid_name} {d.tReply.user.last_name} </b></p><p>Your message : {d.tReply.reply_msg} </p><p>Comment on<h3>Q.{d.tReply.ticket.id} {d.tReply.ticket.question}</h3></p><br/><br/><p>Replied by: <b>{d.userm.first_name} {d.userm.mid_name} {d.userm.last_name}</b> from <b>{d.userm.user_type}</b></p><p>Replied Message : {d.rplymsg}</p>"
        html_message += (q + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False,
                  html_message=html_message)
    return render(request, 'Admin_Ticket_Reply.html', {'Reply_data':Reply_data, 'data':data,'ut':ut, 'msg':msg, 'rid':rid})


def ShowReplyMsgDeveloper(request, id):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    Reply_data = TicketReply.objects.filter(ticket_id=id)
    data = request.session.get('name')
    ut = request.session.get('user_type')
    msg = ""
    if request.method == 'POST':
        d = ReplyToReply()
        d.tReply_id = request.POST['reply_id']
        d.userm_id = request.session['id']
        d.rplymsg = request.POST['rtor']
        d.rplymsgdate = datetime.today()
        d.save()
        msg = "Reply sent...."
        subject = "Tech Assist"
        email_to = d.tReply.user.email
        mail_body = "Hello"
        html_message = """
                        <div style="margin: 0; padding: 0; background: #91b5ec;">
                                            <div style=" border-radius: 30px;
                                        box-shadow: 3px 3px 3px #b1b1b1,
                                                -3px -3px 3px #555;">
                                    <img style="float: left;padding: 10px;" Tech Asisst src="https://www.invoid.co/assets/images/logo_dark_img.png" width="150px">
                                    <ul style="text-align: center;">
                                        <li style="display: inline-block; list-style: none; padding: 20px; font-size: 20px;"><strong>Tech Assist</strong></li>
                                    </ul>
                                </div>

                                <div style="background-color:#f2f1ed; padding:10px;">

                        """
        q = f"<p>Hello <b>{d.tReply.user.first_name} {d.tReply.user.mid_name} {d.tReply.user.last_name} </b></p><p>Your message : {d.tReply.reply_msg} </p><p>Comment on<h3>Q.{d.tReply.ticket.id} {d.tReply.ticket.question}</h3></p><br/><br/><p>Replied by: <b>{d.userm.first_name} {d.userm.mid_name} {d.userm.last_name}</b> from <b>{d.userm.user_type}</b></p><p>Replied Message : {d.rplymsg}</p>"
        html_message += (q + '</div></div>')
        send_mail(subject, mail_body, 'helpdeskricla@gmail.com', [email_to], fail_silently=False,
                  html_message=html_message)
    return render(request, 'Developer_Ticket_Reply.html', {'Reply_data':Reply_data, 'data':data,'ut':ut, 'msg':msg})


def RepliedAdminMsg(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Admin':
        return redirect('/logout/')
    Rdata = ReplyToReply.objects.all()
    data = request.session.get('name')
    ut = request.session.get('user_type')
    Rid = request.session.get('id')
    return render(request, 'Replied_Admin_Comment.html', {'Rdata':Rdata, 'Rid':Rid, 'data':data,'ut':ut})

def RepliedDeveloperMsg(request):
    if request.session.get('name', 'None') == 'None':
        return redirect('/login/')
    if request.session['user_type'] != 'Developer':
        return redirect('/logout/')
    Rdata = ReplyToReply.objects.all()
    data = request.session.get('name')
    ut = request.session.get('user_type')
    Rid = request.session.get('id')
    return render(request, 'Reply_Developer_Comment.html', {'Rdata':Rdata, 'Rid':Rid, 'data':data,'ut':ut})






