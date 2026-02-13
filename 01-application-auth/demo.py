"""Demo script for application authentication."""
import asyncio
from auth_application import ApplicationAuthProvider

async def list_users(client):
    """Example: List all users in tenant."""
    print("\n📋 Listing Users...")
    print("=" * 50)
    
    users = await client.users.get()
    if users and users.value:
        for user in users.value[:10]:  # First 10
            print(f"  • {user.display_name} ({user.user_principal_name})")
        print(f"\nTotal: {len(users.value)} users")

async def get_user_by_id(client, user_id):
    """Example: Get specific user."""
    print(f"\n👤 Getting User: {user_id}")
    print("=" * 50)
    
    user = await client.users.by_user_id(user_id).get()
    if user:
        print(f"  Name: {user.display_name}")
        print(f"  Email: {user.user_principal_name}")
        print(f"  Job: {user.job_title or 'N/A'}")

async def main():
    """Main demo function."""
    print("=" * 50)
    print("Microsoft Graph - Application Auth Demo")
    print("=" * 50)

    # user_if from a CDX tenant demo
    user_id = "45674885-ff25-423b-84c8-f95f949c443d"
    
    try:
        # Setup authentication
        auth = ApplicationAuthProvider()
        
        client = auth.get_client()
        
        # Get users functionalities
        await list_users(client)
        await get_user_by_id(client, user_id)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
