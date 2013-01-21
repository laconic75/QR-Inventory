# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T("George's TV Inventory")

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Joel Robinson <joel@georgestv.net>'
response.meta.description = 'Inventory Appliacation'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu+=[
        (SPAN('Inventory',_style='color:yellow'),False, None, [
                (T('Enter Inventory'),False,URL('qrinv','enter_inventory')),
                (T('Update Inventory'),False,URL('qrinv','update_inventory'))
                ]
         )]
_()

