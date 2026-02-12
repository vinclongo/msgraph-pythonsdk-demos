from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from config import Config

class ApplicationAuthProvider:
    """Handles app-only authentication with Microsoft Graph."""
    
    def __init__(self):
        """Initialize authentication: i.e., create the GraphServiceClient"""
        Config.validate()
        
        # Authentication logic (Application type)
        self.credential = ClientSecretCredential(
            tenant_id=Config.TENANT_ID,
            client_id=Config.CLIENT_ID,
            client_secret=Config.CLIENT_SECRET
        )
        
        self.scopes = ['https://graph.microsoft.com/.default']
        
        self.client = GraphServiceClient(
            credentials=self.credential,
            scopes=self.scopes
        )

    def get_client(self) -> GraphServiceClient:
        """Get authenticated Graph client."""
        return self.client