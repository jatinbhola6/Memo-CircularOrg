from django.db import models
from mongoengine import *
from django.contrib.auth.hashers import make_password
import datetime
import hashlib
from django.core.validators import RegexValidator
# Create your models here.
class Employee(Document):
    designation=StringField(help_text=None)
    department=StringField(help_text=None)
    first_name=StringField(max_length=50,min_length=2,help_text=None)
    last_name=StringField(max_length=50,min_length=2,help_text=None)
    password=StringField(max_length=80,min_length=2,help_text=None)
    emp_uid=StringField(unique=True,help_text='Use This to Log In')
    def create_uid(self,first_emp_with_name):
        now=datetime.datetime.now()
        self.emp_uid=self.first_name+'_'+self.last_name
        if not first_emp_with_name:
            stamp=now.year+now.month+now.day+now.hour+now.minute+now.second+now.microsecond
            self.emp_uid +='_'+str(stamp)
    def create_emp(self,desig,deptt,f_name,l_name,pw,first_emp_with_name):
        self.designation=desig
        self.department=deptt
        self.first_name=f_name
        self.last_name=l_name
        self.password=make_password(password=pw,hasher='bcrypt')
        self.create_uid(first_emp_with_name)
   
class Memo(Document):
    memo_id=StringField(unique=True,help_text=None)
    subject=StringField(max_length=75,help_text=None)
    body=StringField(max_length=200,help_text=None)
    sender=StringField(max_length=25,validators=[RegexValidator(regex='\w+_\w+(_\d)*',message='Invalid Employee UID')],help_text=None)
    reciever=StringField(max_length=25,validators=[RegexValidator(regex='\w+_\w+(_\d)*',message='Invalid Employee UID')],help_text=None)
    temporal_info=DateTimeField(default=datetime.datetime.now(),help_text=None)
    def as_json(self):
        return dict(
                    memo_id=self.memo_id,subject=self.subject,
                    body=self.body,sender=self.sender,reciever=self.reciever,
                    temporal_info=self.temporal_info.ctime()
                    )
    '''parent_memo_id=StringField()
    cc=StringField(max_length=25)
    bcc=ListField(StringField(max_length=25))'''
    def create_memo_uid(self):
        self.memo_id=hashlib.md5((self.sender+self.subject+self.reciever).encode('ascii')).hexdigest()
    def create(self,sender,reciever,subject,body):
        self.sender=sender
        self.reciever=reciever
        self.subject=subject
        self.create_memo_uid()
        self.body=body

class Circular(Document):
    deptts={
            'HR':'Human Resources',
            'IT':'IT Support',
            'TT':'Technical Team',
            'SM':'Sales and Marketting',
            'SS':'Support Staff'   
            }
    subject=models.CharField(max_length=75)
    body=models.CharField(max_length=300)
    issued_by=EmbeddedDocumentField('Employee')
    issued_under_dep=StringField(choices=deptts.keys())
    temporal_info=models.DateTimeField(auto_now_add=True)
    ackn_by=ListField(EmbeddedDocumentField('Employee'))

