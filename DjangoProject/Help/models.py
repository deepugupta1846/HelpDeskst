from django.db import models

# Create your models here.
USERTYPE = (
    ('Business team', 'Business team'),
    ('Developer', 'Developer'),
    ('Admin', 'Admin'),
    ('ML', 'ML'),
    ('Quality Check', 'Quality Check'),
    ('Tester', 'Tester')
)


class UserModel(models.Model):
    first_name = models.CharField(max_length=100)
    mid_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.CharField(max_length=100, choices=USERTYPE)
    password = models.CharField(max_length=100, default=None)
    approved_by = models.CharField(max_length=100, null=True, blank=True)
    approved_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True )
    revoked_by = models.IntegerField(max_length=3, null=True, blank=True)
    revoke_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.first_name}-{self.mid_name}-{self.last_name}-{self.email}-{self.password}"


class LoginHistory(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    login_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    logout_on = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return f"{self.id}-{self.user}-{self.login_at}-{self.logout_on}"


CATEGORIES = (
    ('Backend', 'Backend'),
    ('Fronted', 'Frontend'),
    ('Android', 'Android')
)
TICKET_TYPE = (
    ('New Devlopment', 'New Devlopment'),
    ('Update', 'Update'),
    ('Bug', 'Bug')
)


class TicketModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True)
    categrories = models.CharField(max_length=100, choices=CATEGORIES)
    ticket_type = models.CharField(max_length=100, choices=TICKET_TYPE)
    question = models.CharField(max_length=250)
    description = models.TextField(null=True)
    ticket_raise_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    ticket_opened_by = models.IntegerField(null=True)
    ticket_closed_by = models.IntegerField(null=True)
    ticket_open_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    ticket_close_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return f"{self.id}-{self.user}-{self.status}-{self.categrories}-{self.ticket_type}-{self.question}-{self.description}-{self.ticket_raise_date}"


class TicketReply(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE)
    reply_msg = models.TextField()
    reply_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    rply_to_rply = models.TextField(null=True)
    rply_to_rply_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return f"{self.id}-Ticket:ID{self.ticket_id}-User:ID-{self.ticket.user.id}-User.Name-{self.ticket.user.first_name}"