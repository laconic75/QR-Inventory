# coding: utf8
db.define_table('invent',
   Field('partnum',unique=True),
   Field('manuf'),
   Field('description'),
   Field('whol_price', 'double'),
   Field('ret_price', 'double'),
   Field('grjr_van', 'integer', default=0),
   Field('josh_van', 'integer', default=0),
   Field('gar_van', 'integer', default=0),
   Field('john_van', 'integer', default=0),
   Field('shop', 'integer', default=0),
   Field('total_stock',compute=lambda r: r['grjr_van'] + r['josh_van'] + r['gar_van'] + r['john_van'] + r['shop']),
   Field('locaton')
   )
