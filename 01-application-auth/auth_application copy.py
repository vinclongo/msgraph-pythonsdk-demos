import asyncio 

from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from config import Config

# Validate environment variables
Config.validate()

# Create a credential object. Used to authenticate requests
credential = ClientSecretCredential(
    tenant_id=Config.TENANT_ID,
    client_id=Config.CLIENT_ID,
    client_secret=Config.CLIENT_SECRET
)
scopes = ['https://graph.microsoft.com/.default']

# Create an API client with the credentials and scopes.
client = GraphServiceClient(credentials=credential, scopes=scopes)

# put a valid user-id
user_id = "45674885-ff25-423b-84c8-f95f949c443d"

# GET A USER USING THE USER ID (GET /users/{id})
async def get_user():
    user = await client.users.by_user_id(user_id).get()
    if user:
        print(user.user_principal_name, user.display_name, user.id)
asyncio.run(get_user())