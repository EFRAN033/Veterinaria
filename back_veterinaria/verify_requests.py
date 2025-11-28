import json
import sys
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000/api/v1"

def request(method, url, data=None, headers=None):
    if headers is None:
        headers = {}
    
    if data:
        data_bytes = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    else:
        data_bytes = None
        
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status >= 200 and response.status < 300:
                return json.loads(response.read().decode('utf-8'))
            else:
                print(f"Error {response.status}: {response.read().decode('utf-8')}")
                return None
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        if e.code == 401: # Auth error
             sys.exit(1)
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def login(email, password):
    # Auth endpoint expects JSON LoginDTO
    data = {"email": email, "password": password}
    return request("POST", f"{BASE_URL}/auth/login", data)["access_token"]

def create_request(token, type, data):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "service_type": type,
        "estimated_cost": 100.0,
        "service_data": data,
        "images": []
    }
    
    if type in ["aesthetic", "general", "consultation"]:
        payload["pet_name"] = data.get("petName", "Unknown")
        
    print(f"Creating {type} request...")
    return request("POST", f"{BASE_URL}/service-requests/", payload, headers)

def get_vet_requests(token):
    headers = {"Authorization": f"Bearer {token}"}
    return request("GET", f"{BASE_URL}/service-requests/?status=pending", None, headers)

def main():
    print("Starting verification...")
    try:
        user_token = login("usuario@test.com", "usuario123")
        vet_token = login("veterinario@test.com", "veterinario123")
    except Exception as e:
        print(f"Login error: {e}")
        return

    print("Logged in successfully.")

    reqs = []
    
    # General
    gen_data = {"serviceType": "vacunacion", "petName": "Firulais", "preferredDate": "2023-12-01", "notes": "Test General"}
    r = create_request(user_token, "general", gen_data)
    if r: reqs.append(r)

    # Clinical
    clin_data = {"description": "Test Clinical Case", "history": "None", "isFollowUp": False}
    r = create_request(user_token, "clinical", clin_data)
    if r: reqs.append(r)

    # Aesthetic
    aes_data = {"petName": "Luna", "breed": "Poodle", "species": "perro", "services": [{"type": "baño", "instructions": "Careful"}]}
    r = create_request(user_token, "aesthetic", aes_data)
    if r: reqs.append(r)

    # Verify
    vet_requests = get_vet_requests(vet_token)
    if not vet_requests:
        print("Failed to fetch vet requests.")
        return

    print(f"\nVet sees {len(vet_requests)} pending requests.")
    
    found_ids = [r['id'] for r in vet_requests]
    
    all_found = True
    for req in reqs:
        if req['id'] in found_ids:
            print(f"✅ Request {req['id']} ({req['service_type']}) found in dashboard.")
        else:
            print(f"❌ Request {req['id']} ({req['service_type']}) NOT found in dashboard.")
            all_found = False
            
    if all_found and len(reqs) > 0:
        print("\nSUCCESS: All created requests are visible to the veterinarian.")
    else:
        print("\nFAILURE: Some requests are missing or none created.")

if __name__ == "__main__":
    main()
