import happybase

connection = happybase.Connection('107.22.78.179')
table = connection.table('ticket')

for key, data in table.scan(row_prefix='83k4'):
    print key, data

