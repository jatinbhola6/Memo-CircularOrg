'''
Created on 01-Sep-2016

@author: jatinbhola6
'''
from mongodbforms import DocumentForm
from MnCApp.models import *
from django.forms.widgets import Select, PasswordInput, HiddenInput, Textarea
from django import forms
from django.forms.fields import CharField
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password
from django.db.models.fields import TextField

'''import re
from django.core.exceptions import ValidationError
def validate_hash(value):
    reg=re.compile('\w+_\w+_\d+')
    if not reg.match(value):
        raise ValidationError('Invalid Employee UID')'''
class SignUpForm(DocumentForm):
    class Meta:
        desigs=(
        ('D','Director'),
        ('GM','General Manager'),
        ('AM','Assistant Manager'),
        ('A','Associates')
            )
        deptts=(
                ('HR','Human Resources'),
                ('IT','IT Support'),
                ('TT','Technical Team'),
                ('SM','Sales and Marketting'),
                ('SS','Support Staff')
                )
        document=Employee
        widgets={
                 'designation':Select(choices=desigs),
                 'department':Select(choices=deptts),
                 'password':PasswordInput(),
                 'emp_uid':HiddenInput()
                 }
    conf_pass=forms.CharField(widget=PasswordInput())
    def clean(self):
        cleaned_data=super(SignUpForm,self).clean()
        if cleaned_data['first_name']==None :
            self.add_error(None,'length panga')    
        if cleaned_data['password']!=cleaned_data['conf_pass']:
            self.add_error(None,'length panga')
    
    def save(self,commit=True):
        new_emp=Employee()
        no_of_same_name_emp=Employee.objects.filter(first_name=self.cleaned_data['first_name'],last_name=self.cleaned_data['last_name']).count()
        if no_of_same_name_emp>=1:
            print('More employee with same name already Employed')
            first_emp_with_name=False
        else:
            first_emp_with_name=True
        new_emp.create_emp(self.cleaned_data['designation'], self.cleaned_data['department'],
                            self.cleaned_data['first_name'],self.cleaned_data['last_name'],
                             self.cleaned_data['password'],first_emp_with_name
                             )
        if commit:
            new_emp.save()
        return new_emp

class SignInForm(forms.Form):
    user_id=forms.RegexField(regex='\w+_\w+(_\d)*',error_message="Invalid User ID",label="User ID",widget=forms.TextInput(attrs={'class':'form-control','required':True}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','required':True}))
    e_obj=Employee()
    def clean(self):
        try:
            self.e_obj=Employee.objects.get(emp_uid=self.cleaned_data['user_id'])
        except KeyError:
            self.add_error(None,'Invalid User Id')
        except DoesNotExist:
            self.add_error(None,'No User found')
        if check_password(self.cleaned_data['password'],self.e_obj.password)== False:
            self.add_error(None,"Username or Password Doesn't Match")
    def log_in(self):
        return self.e_obj

class Memo_Compose(DocumentForm):
    class Meta:
        document=Memo
        widgets={
                'memo_id':HiddenInput(),
                'body':Textarea(),
                'sender':HiddenInput(),
                'temporal_info':HiddenInput()
                #'parent_memo_id':HiddenInput(),
                }
    def clean(self):
        if (self.cleaned_data['reciever']==None or self.cleaned_data['reciever']=='' ):
            self.add_error('reciever','Enter recieving employee')
    def save(self,sid,commit=True):
        new_memo=Memo()
        new_memo.create(sender=sid,reciever=self.cleaned_data['reciever'],
                        subject=self.cleaned_data['subject'],body=self.cleaned_data['body'])
        if commit==True:
            new_memo.save()
        return new_memo.memo_id