import pusher
app_id = 'XXXXX'
key = 'XXXXXXXXXXXXXXXXXXXX'
secret = 'XXXXXXXXXXXXXXXXXXXX'

p = pusher.Pusher(app_id=app_id, key=key, secret=secret)
p['test_channel'].trigger('myevent', 'hello')
