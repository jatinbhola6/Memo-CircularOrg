'''
Created on 02-Sep-2016

@author: jatinbhola6
'''
from django import template
register=template.Library()

@register.filter(name='key')
def key(dict,key):
    return dict[key]