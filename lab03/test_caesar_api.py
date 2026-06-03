from api import app

if __name__ == '__main__':
    client = app.test_client()
    resp = client.post('/api/caesar/encrypt', json={'plain_text':'Hello, World!', 'key':3})
    print('ENCRYPT status:', resp.status_code, 'body:', resp.get_json())
    encrypted = resp.get_json().get('encrypted_message')

    resp2 = client.post('/api/caesar/decrypt', json={'cipher_text': encrypted, 'key':3})
    print('DECRYPT status:', resp2.status_code, 'body:', resp2.get_json())
