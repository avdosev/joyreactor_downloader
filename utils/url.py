import base64

def gen_url(key):
    publicKey = base64.b64decode(key.encode('utf-8')).decode('utf-8')
    type_, id_ = publicKey.lower().split(':')
    return 'https://m.joyreactor.cc/{}/{}'.format(type_, id_)