import requests

BASE_URL = 'http://127.0.0.1:5000/api/'

def register_user_request(username, email, password, full_name, bio, country_code, phone_number, is_public, profile_image):
    return requests.post(
        BASE_URL + 'register',
        json={
            'username': username,
            'email': email,
            'password': password,
            'full_name': full_name,
            'bio': bio,
            'country_code': country_code,
            'phone_number': phone_number,
            'is_public': is_public,
            'profile_image': profile_image
        }
    )


def delete_user_request(username):
    return requests.delete(BASE_URL + f'users/{username}')


def get_country_by_code(alpha2):
    return requests.get(BASE_URL + f'country/{alpha2}')


def get_all_countries():
    return requests.get(BASE_URL + 'countries')


def run_api_tests():
    user_response = register_user_request(
        username='test_user',
        email='test@example.com',
        password='securepass',
        full_name='Test User',
        bio='Test bio',
        country_code='US',
        phone_number='+1234567890',
        is_public=True,
        profile_image='http://example.com/profile.jpg'
    )
    print(user_response.json())
    assert user_response.status_code == 201
    print("Register user success!")

    countries_response = get_all_countries()
    assert countries_response.status_code == 200
    print("Get all countries passed!")

    country_response = get_country_by_code('US')
    assert country_response.status_code == 200
    print("Get country by alpha2 passed!")

    #delete_response = delete_user_request('test_user')
    #assert delete_response.status_code == 200
    #print("Delete user passed!")


if __name__ == '__main__':
    run_api_tests()
