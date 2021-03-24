"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', login),
    path('signup/', signup),
    path('devloper/', userpage),
    path('logout/', logout),
    path('userprofile/', profile),
    path('businessprofile/', businessprofile),
    path('adminpage/', adminPage),
    path('adminprofile/', adminprofile),
    path('viewnewrequest/', view_all_request),
    path('viewnewrequest/delete/<int:id>/', reject),
    path('viewnewrequest/update/<int:id>/', accept),
    path('business/', business),
    path('viewapprovel/', view_Approvel),
    path('viewapprovel/revoke/<int:id>/', revoke),
    path('allrevokeuser/', allrevokeusers),
    path('alluser/', all_user),
    path('loginhistory/', logInHistory),
    path('ticketraise/', newticketRaise),
    path('showraiseticket/', showRaiseTicket),
    path('otpvalidation/', otpvalidation),
    path('emailinput/', emailinput),
    path('showraiseticket/delete/<int:id>/', deleteTicket),
    path('newraiseticket/status/<int:id>/', ticketopen),
    path('newraiseticketbyadmin/status/<int:id>/', ticketopenbyadmin),
    path('newraisedticket/', newRaisedTicket),
    path('newraisedticketadmin/', newRaisedTicketinadmin),
 
    path('repliedmsg/', show_replied_msg),
    path('status/<int:id>/', ticketclosed),
    path('admin/status/<int:id>/', ticketclosedbyadmin),
    path('showclosedticket/', showclosedTicket),
    path('showclosedticketadmin/', showclosedTicketinAdmin),
    path('mlpage/', MLpage),
    path('QualityCheck/', Quality_Check),
    path('Tester/', Tester),
    path('adminpage/<int:ticket_opened_by>/', showOpenedbyname),
    path('developer/<int:ticket_opened_by>/', showOpenedbynamedeveloper),
    path('business/<int:ticket_opened_by>/', showOpenedbynamebusiness),
    path('adminpage/<int:approved_by>/', showApprovedby)

]
