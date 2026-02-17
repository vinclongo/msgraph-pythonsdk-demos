"""Demo script for delegated authentication."""
import asyncio
from auth_delegated import DelegatedAuthProvider

        
async def get_me(client):
    me = await client.me.get()

    if me:
        print(f"  Name: {me.display_name}")
        print(f"  Email: {me.user_principal_name}")
        print(f"  Job: {me.job_title or 'N/A'}")

async def main():
    """Main demo function."""
    print("=" * 50)
    print("Microsoft Graph - Delegated Auth Demo")
    print("=" * 50)

    # user_if from a CDX tenant demo
    user_id = "45674885-ff25-423b-84c8-f95f949c443d"
    
    try:        
        # chose the authN Mode: device_code or browser
        
        auth = DelegatedAuthProvider(auth_type = "device_code")
        #auth = DelegatedAuthProvider(auth_type = "browser")

        client = auth.get_client()
        
        # Get users functionalities
        await get_me(client)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
