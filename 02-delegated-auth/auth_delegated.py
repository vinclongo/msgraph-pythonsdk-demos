from azure.identity import DeviceCodeCredential, InteractiveBrowserCredential
from msgraph import GraphServiceClient
from config import Config
from typing import Literal

class DelegatedAuthProvider:
    """Handles delegated authentication with Microsoft Graph using DeviceCode and InteractiveBrowser Flow"""
    
    def __init__(self, auth_type: Literal['device_code', 'browser'] = 'device_code'):
        """
        Initialize delegated authentication.
        
        Args:
            auth_type: Authentication method to use
                - 'device_code': For CLI/headless scenarios (DEFAULT)
                - 'browser': For desktop apps with browser
        """
        Config.validate()
        
        # Authentication logic (Delegated type)
        if auth_type == "device_code":
            self.credential = DeviceCodeCredential(
                tenant_id=Config.TENANT_ID,
                client_id=Config.CLIENT_ID,
            )
        elif auth_type == "browser":
            self.credential = InteractiveBrowserCredential(
                tenant_id=Config.TENANT_ID,
                client_id=Config.CLIENT_ID,
            )
        else:
            raise ValueError(f"Invalid auth_type: {auth_type}")
            
        
        self.scopes = Config.GRAPH_SCOPES
        
        self.client = GraphServiceClient(
            credentials=self.credential,
            scopes=self.scopes
        )

    def get_client(self) -> GraphServiceClient:
        """Get authenticated Graph client."""
        return self.client
    
