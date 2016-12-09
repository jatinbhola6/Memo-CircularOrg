from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import  TemplateView
from django.http.response import  HttpResponseRedirect, HttpResponse
from .forms import *
from django.views.generic.edit import FormView
from django.core import serializers
import json
from django.shortcuts import render
# Create your views here.

def index(request):
    if 'key' in request.session:
        return HttpResponseRedirect(reverse_lazy('MnCapp:success'))
    else : 
        return HttpResponseRedirect(reverse_lazy('MnCapp:signin'))
def test(request):
    return render(request,'MnCApp/index.html')
class SignUpView(FormView):
    template_name='MnCApp/signup.html'
    form_class=SignUpForm
    
    def form_valid(self,form):
        emp_obj=form.save()
        self.request.session['key']=emp_obj.emp_uid
        return HttpResponseRedirect(reverse_lazy('MnCapp:success'))
class SuccessView(TemplateView):
    template_name='MncApp/base.html'
    def dispatch(self,request):
        if 'key' not in self.request.session:
            return HttpResponseRedirect(reverse_lazy('MnCapp:signin'))
       
        return super(SuccessView,self).dispatch(request)
        
    def get_context_data(self, **kwargs):
        context=super(SuccessView,self).get_context_data(**kwargs)
        eid=(self.request.session['key'])
        emp_obj=Employee.objects.get(emp_uid=eid)
        memo_list=Memo.objects.filter(reciever=self.request.session['key']).order_by('-temporal_info')
        context={
                 'emp':emp_obj,
                 'memo_list':memo_list,
                 'desigs':{
                           'D':'Director',
                           'GM':'General Manager',
                           'AM':'Assistant Manager',
                           'A':'Associates'
                        },
                 'deptts':{
                           'HR':'Human Resources',
                           'IT':'IT Support',
                           'TT':'Technical Team',
                           'SM':'Sales and Marketting',
                           'SS':'Support Staff'
                           }
                 }
        if 'memo' in self.request.session:
            context['mid']=self.request.session['memo']
                 
        return context
    
class SignInView(FormView):
    
    template_name='MnCApp/index.html'
    form_class=SignInForm
    def form_valid(self, form):
        emp_obj=form.log_in()
        self.request.session['key']=emp_obj.emp_uid
        return HttpResponseRedirect(reverse_lazy('MnCapp:success'))
    
def log_out(request):
    if 'key' in request.session: 
        del request.session['key']
    if 'memo' in request.session:
        del request.session['memo']
    return HttpResponseRedirect(reverse_lazy('MnCapp:signin'))

class MemoView(FormView):
    template_name='MnCApp/memo_comp.html'
    form_class=Memo_Compose
    success_url=reverse_lazy('MnCapp:success')
    def form_valid(self, form):
        mid=form.save(self.request.session['key'])
        self.request.session['memo']=mid
        return HttpResponseRedirect(reverse_lazy('MnCapp:success'))
    
def getMemo(request):
    if request.method=='POST':
        mid=request.POST['memo_id']
        memo_obj=Memo.objects.get(memo_id=str(mid))
        return HttpResponse(json.dumps(memo_obj.as_json()),content_type="application/json")