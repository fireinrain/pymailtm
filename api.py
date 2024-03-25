import aiohttp

from exception import TmBaseException, UnauthorizedException


class MessageReceivedHandler:
    def handle(self, msg: str):
        print(f"handle message here")
        print(msg)


class SimpleMessageReceivedHandler(MessageReceivedHandler):
    def handle(self, msg: str):
        super().handle(msg)
        print(f"handle message...")


# here are mailtm api
class MailTMApi:
    def __init__(self):
        self.base_url = 'https://api.mail.tm'
        self.email = None
        self.password = None
        self.token = None
        self.domain_url = f'{self.base_url}/domains'
        self.accounts_url = f'{self.base_url}/accounts'
        self.me_url = f'{self.base_url}/me'
        self.messages_url = f'{self.base_url}/messages'
        self.source_url = f'{self.base_url}/sources'
        self.token_url = f'{self.base_url}/token'
        self.on_message_received_url = f'https://mercure.mail.tm/.well-known/mercure'

    # "hydra:member": [
    #     {
    #       "@id": "string",
    #       "@type": "string",
    #       "@context": "string",
    #       "id": "string",
    #       "domain": "string",
    #       "isActive": true,
    #       "isPrivate": true,
    #       "createdAt": "2022-04-01T00:00:00.000Z",
    #       "updatedAt": "2022-04-01T00:00:00.000Z"
    #     }
    #   ]
    async def get_domains(self, page=1) -> {}:
        params = {'page': page}
        async with aiohttp.ClientSession as session:
            async with session.get(self.domain_url, params=params) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "@id": "string",
    #   "@type": "string",
    #   "@context": "string",
    #   "id": "string",
    #   "domain": "string",
    #   "isActive": true,
    #   "isPrivate": true,
    #   "createdAt": "2022-04-01T00:00:00.000Z",
    #   "updatedAt": "2022-04-01T00:00:00.000Z"
    # }
    async def get_domain(self, domain_id: str) -> {}:
        async with aiohttp.ClientSession as session:
            async with session.get(self.domain_url + f"/{domain_id}") as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "@context": "string",
    #   "@id": "string",
    #   "@type": "string",
    #   "id": "string",
    #   "address": "user@example.com",
    #   "quota": 0,
    #   "used": 0,
    #   "isDisabled": true,
    #   "isDeleted": true,
    #   "createdAt": "2022-04-01T00:00:00.000Z",
    #   "updatedAt": "2022-04-01T00:00:00.000Z"
    # }
    async def create_accounts(self, email, password) -> {}:
        form_data = {'address': email, 'password': password}
        async with aiohttp.ClientSession as session:
            async with session.post(self.accounts_url, data=form_data) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "id": "string",
    #   "token":"string"
    # }
    async def get_token(self, email, password) -> {}:
        form_data = {'address': email, 'password': password}
        async with aiohttp.ClientSession as session:
            async with session.post(self.token_url, data=form_data) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "@context": "string",
    #   "@id": "string",
    #   "@type": "string",
    #   "id": "string",
    #   "address": "user@example.com",
    #   "quota": 0,
    #   "used": 0,
    #   "isDisabled": true,
    #   "isDeleted": true,
    #   "createdAt": "2022-04-01T00:00:00.000Z",
    #   "updatedAt": "2022-04-01T00:00:00.000Z"
    # }
    async def get_account(self, account_id: str) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        async with aiohttp.ClientSession as session:
            async with session.post(self.accounts_url + f'/{account_id}', headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    async def delete_account(self, account_id) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        async with aiohttp.ClientSession as session:
            async with session.delete(self.accounts_url + f'/{account_id}', headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "@context": "string",
    #   "@id": "string",
    #   "@type": "string",
    #   "id": "string",
    #   "address": "user@example.com",
    #   "quota": 0,
    #   "used": 0,
    #   "isDisabled": true,
    #   "isDeleted": true,
    #   "createdAt": "2022-04-01T00:00:00.000Z",
    #   "updatedAt": "2022-04-01T00:00:00.000Z"
    # }
    async def get_me(self) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        async with aiohttp.ClientSession as session:
            async with session.get(self.me_url, headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "hydra:member": [
    #     {
    #       "@id": "string",
    #       "@type": "string",
    #       "@context": "string",
    #       "id": "string",
    #       "accountId": "string",
    #       "msgid": "string",
    #       "from": {
    #           "name": "string",
    #           "address": "string"
    #       },
    #       "to": [
    #         {
    #             "name": "string",
    #             "address": "string"
    #         }
    #       ],
    #       "subject": "string",
    #       "intro": "string",
    #       "seen": true,
    #       "isDeleted": true,
    #       "hasAttachments": true,
    #       "size": 0,
    #       "downloadUrl": "string",
    #       "createdAt": "2022-04-01T00:00:00.000Z",
    #       "updatedAt": "2022-04-01T00:00:00.000Z"
    #     }
    #   ],
    #   "hydra:totalItems": 0,
    #   "hydra:view": {
    #     "@id": "string",
    #     "@type": "string",
    #     "hydra:first": "string",
    #     "hydra:last": "string",
    #     "hydra:previous": "string",
    #     "hydra:next": "string"
    #   },
    #   "hydra:search": {
    #     "@type": "string",
    #     "hydra:template": "string",
    #     "hydra:variableRepresentation": "string",
    #     "hydra:mapping": [
    #       {
    #         "@type": "string",
    #         "variable": "string",
    #         "property": "string",
    #         "required": true
    #       }
    #     ]
    #   }
    # }
    async def get_messages(self, page=1) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        params = {'page': page}
        async with aiohttp.ClientSession as session:
            async with session.get(self.messages_url, headers=headers, params=params) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "@context": "string",
    #   "@id": "string",
    #   "@type": "string",
    #   "id": "string",
    #   "accountId": "string",
    #   "msgid": "string",
    #     "from": {
    #         "name": "string",
    #       "address": "string"
    #   },
    #   "to": [
    #         {
    #             "name": "string",
    #             "address": "string"
    #         }
    #     ],
    #   "cc": [
    #     "string"
    #   ],
    #   "bcc": [
    #     "string"
    #   ],
    #   "subject": "string",
    #   "seen": true,
    #   "flagged": true,
    #   "isDeleted": true,
    #   "verifications": [
    #     "string"
    #   ],
    #   "retention": true,
    #   "retentionDate": "2022-04-01T00:00:00.000Z",
    #   "text": "string",
    #   "html": [
    #     "string"
    #   ],
    #   "hasAttachments": true,
    #   "attachments": [
    #     {
    #       "id": "string",
    #       "filename": "string",
    #       "contentType": "string",
    #       "disposition": "string",
    #       "transferEncoding": "string",
    #       "related": true,
    #       "size": 0,
    #       "downloadUrl": "string"
    #     }
    #   ],
    #   "size": 0,
    #   "downloadUrl": "string",
    #   "createdAt": "2022-04-01T00:00:00.000Z",
    #   "updatedAt": "2022-04-01T00:00:00.000Z"
    # }
    async def get_message(self, message_id: str) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        async with aiohttp.ClientSession as session:
            async with session.get(self.messages_url + f'/{message_id}', headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    async def delete_message(self, message_id: str) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        async with aiohttp.ClientSession as session:
            async with session.delete(self.messages_url + f'/{message_id}', headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "seen": true
    # }
    async def update_message_as_read(self, message_id: str) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        async with aiohttp.ClientSession as session:
            async with session.patch(self.messages_url + f'/{message_id}', headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    # {
    #   "@context": "string",
    #   "@id": "string",
    #   "@type": "string",
    #   "id": "string",
    #   "downloadUrl": "string",
    #   "data": "string"
    # }
    async def get_source(self, source_id: str) -> {}:
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token}
        async with aiohttp.ClientSession as session:
            async with session.patch(self.source_url + f'/{source_id}', headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                return await response.json()

    def on_message_receive(self, account_id: str, messageHandler: MessageReceivedHandler):
        '''
        For each listened message, there will be an Account event.
        That Account is the Account resource that received the message, with updated "used" property.
        /accounts/{id}
        :return:
        '''
        if self.token is None:
            raise UnauthorizedException()
        headers = {'Authorization': 'Bearer ' + self.token,
                   'Accept': 'text/event-stream'}

        async with aiohttp.ClientSession as session:
            async with session.get(self.on_message_received_url + f'/accounts/{account_id}',
                                   headers=headers) as response:
                TmBaseException.check_result_status(response.status)
                event_type = None
                data = None
                async for line in response.content:
                    text = line.decode().strip()
                    if text.startswith('event:'):
                        event_type = text.replace('event:', '').strip()
                        if event_type == 'Account':
                            messageHandler.handle(text)
                    elif text.startswith('data:'):
                        data = text.replace('data:', '').strip()
                    elif text == '':
                        # An empty line denotes the end of an event.
                        if event_type and data:
                            print(f"Event type: {event_type}, Data: {data}")
                            # Reset event_type and data for the next event
                            event_type = None
                            data = None
