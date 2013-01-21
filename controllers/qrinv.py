# QR inventory system
# 06/01/2012
# Joel Robinson

from elaphe import barcode
from gluon.contenttype import contenttype
if 0:
    from gluon.globals import *
    from gluon.html import *
    from gluon.http import *
    from gluon.sqlhtml import SQLFORM, SQLTABLE, form_factory
    session = Session()
    request = Request()
    response = Response()
    from gluon.sql import *
    from gluon.validators import *
    from db import * 

def qrgen():
    "Create QR codes"
    image = IMG(_src=URL('static/images', 'none.png'), _alt="none")
    form = SQLFORM.factory(
        Field('message', requires=IS_NOT_EMPTY())
        )
    if form.accepts(request.vars, session):                        
        msg=request.vars.message               
        session.msg=request.vars.message
        image = IMG(_src=URL('qrcode',vars={'message':msg}))
        return dict(form=form,image=image)
    else:
        return dict(form=form,image=image)
        
def qrcode():
    # take session.msg and return equivilent QR code
    qrcode=barcode('qrcode', session.msg, options=dict(version=5, eclevel='M'),
        margin=10, data_mode='8-bits')
    response.headers['Content-Type']="image/png"
    qrcode.save(response.body, "PNG")
    return response.body.getvalue()

@auth.requires_login()    
def manage():
    # manage inventory database
    table=db.invent
    form = crud.update(table,request.args(1))
    #table.id.represent = lambda id, row: \
    #   A('edit:',id,_href=URL(args=(request.args(1),id)))
    table.id.represent = lambda id, row: A('edit:',id,_href=URL('confirm_inventory',vars= {'ident':id} ))
    search, rows = crud.search(table)
    return dict(form=form,search=search,rows=rows)

def set_record(form):
    #helper furnction with enter_inventory
    #can't put session var in enter_inventory or will return error if not set
    session.record = form.vars.id

@auth.requires_login()
def enter_inventory():      
    form = crud.create(db.invent, next=URL('confirm_inventory'), \
        onaccept= lambda form : set_record(form), message=T("record created"))
    return dict(form=form)

@auth.requires_login()    
def confirm_inventory():
    # shows record just entered in enter_inventory    
    #record = crud.read(db.invent,request.ident)
    record = crud.read(db.invent,session.record) 
    # if session.record else "You have to enter a record first"
    controller= request.env.path_info.strip("confirm_inventory")
    page = "update_inventory?partnum="
    location = "http://"+request.env.server_name+controller+page+record.record.partnum
    session.msg=location    
    image = IMG(_src=URL('qrcode', vars={'location':location}),_id="qrcode")    
    return dict(record=record,image=image)

@auth.requires_login()
def view_inventory():
    # query for partnum
    # partnum should be in html request
    # ex. view_inventory?partnum=LAMP-1
    row = db(db.invent.partnum == request.get_vars.partnum).select().first()
    # display queried object
    record = crud.read(db.invent, row.id)
    return dict(record=record)

def qr_request():
    if (request.vars.partnum == None):
        if(session.partnum != None):
            redirect(URL('update_inventory'))
        else:
            record = 'No part number URL should read "update_inventory?partnum=something"'
            return dict(record=record)
    else:
        session.partnum = request.vars.partnum
        redirect(URL('update_inventory'))

@auth.requires_login()    
def update_inventory():
    db.invent.partnum.writable = False
    db.invent.manuf.writable = False
    db.invent.description.writable = False
    db.invent.whol_price.writable = False
    db.invent.ret_price.writable = False
    crud.settings.update_deletable = False 
    if request.get_vars.partnum:
        row = db(db.invent.partnum == request.get_vars.partnum).select().first()
        return dict(total = row.total_stock,row=row, record=crud.update(db.invent, row.id) if row
            else 'Part #%s not found' % request.get_vars.partnum) 
    else:
        row = None
        return dict(row=row, record="No part number. URL should read update_inventory?partnum=12345")
