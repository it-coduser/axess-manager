import requests


class AXESS:
    def __init__(self, account):
        self.connection = requests.Session()
        self.rest_url = account.rest_url
        self.account = account

    def execute(self, method, payload):
        key, data = payload.popitem()

        if not self.account.session:
            self.account.new_session()

        session = self.account.session

        data.update({'NSESSIONID': str(session)})

        response = self.connection.post(f'{self.rest_url}/{method}', json={
            key: data
        })

        return session, data, response

    def create_session(self):
        response = self.connection.post(f'{self.rest_url}/login', json={
            'i_ctLoginReq': {
                'SZCOUNTRYCODE': 'EN',
                'SZLOGINMODE': 'CUSTOMER',
                'SZLOGINID': self.account.login_id,
                'SZUSERNAME': self.account.username,
                'SZPASSWORD': self.account.password,
                'SZSOAPUSERNAME': self.account.soap_username,
                'SZSOAPPASSWORD': self.account.soap_password,
            }
        })

        if response.status_code != 200:
            return None

        data = response.json()

        _, result = data.popitem()

        if result['NERRORNO'] != 0:
            return None

        session_id = result['NSESSIONID']

        return session_id

    def check_session(self, session):
        response = self.connection.post(f'{self.rest_url}/checkSession', json={
            'i_ctCheckSessionReq': {
                'NSESSIONID': session.session_id,
            }
        })

        if response.status_code != 200:
            return False

        data = response.json()

        _, result = data.popitem()

        return result['NERRORNO'] == 0

    def delete_session(self, session):
        response = self.connection.post(f'{self.rest_url}/logout', json={
            'i_ctLogoutReq': {
                'NSESSIONID': session.session_id,
                'SZSOAPUSERNAME': session.account.soap_username,
                'SZSOAPPASSWORD': session.account.soap_password,
            }
        })

        return response.status_code == 200
