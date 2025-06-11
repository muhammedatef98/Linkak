import requests
import json
import sys
import time

def test_api(base_url):
    print("Testing LinkHub API...")
    
    # Test registration
    print("\n1. Testing user registration...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/register", json=register_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Registration test passed")
        else:
            print("❌ Registration test failed")
    except Exception as e:
        print(f"❌ Registration test error: {str(e)}")
    
    # Test login
    print("\n2. Testing user login...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Login test passed")
            cookies = response.cookies
        else:
            print("❌ Login test failed")
            cookies = None
    except Exception as e:
        print(f"❌ Login test error: {str(e)}")
        cookies = None
    
    # Test profile retrieval
    if cookies:
        print("\n3. Testing profile retrieval...")
        try:
            response = requests.get(f"{base_url}/api/profile", cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ Profile retrieval test passed")
            else:
                print("❌ Profile retrieval test failed")
        except Exception as e:
            print(f"❌ Profile retrieval test error: {str(e)}")
        
        # Test link creation
        print("\n4. Testing link creation...")
        link_data = {
            "title": "Test Link",
            "url": "https://example.com",
            "description": "This is a test link"
        }
        
        try:
            response = requests.post(f"{base_url}/api/links", json=link_data, cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 201:
                print("✅ Link creation test passed")
                link_id = response.json().get('link', {}).get('id')
            else:
                print("❌ Link creation test failed")
                link_id = None
        except Exception as e:
            print(f"❌ Link creation test error: {str(e)}")
            link_id = None
        
        # Test link retrieval
        print("\n5. Testing link retrieval...")
        try:
            response = requests.get(f"{base_url}/api/links", cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ Link retrieval test passed")
            else:
                print("❌ Link retrieval test failed")
        except Exception as e:
            print(f"❌ Link retrieval test error: {str(e)}")
        
        # Test link update
        if link_id:
            print("\n6. Testing link update...")
            update_data = {
                "title": "Updated Test Link",
                "description": "This is an updated test link"
            }
            
            try:
                response = requests.put(f"{base_url}/api/links/{link_id}", json=update_data, cookies=cookies)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ Link update test passed")
                else:
                    print("❌ Link update test failed")
            except Exception as e:
                print(f"❌ Link update test error: {str(e)}")
            
            # Test link deletion
            print("\n7. Testing link deletion...")
            try:
                response = requests.delete(f"{base_url}/api/links/{link_id}", cookies=cookies)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ Link deletion test passed")
                else:
                    print("❌ Link deletion test failed")
            except Exception as e:
                print(f"❌ Link deletion test error: {str(e)}")
        
        # Test logout
        print("\n8. Testing user logout...")
        try:
            response = requests.post(f"{base_url}/api/logout", cookies=cookies)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ Logout test passed")
            else:
                print("❌ Logout test failed")
        except Exception as e:
            print(f"❌ Logout test error: {str(e)}")
    
    print("\nAPI Testing Complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5000"
    
    test_api(base_url)
