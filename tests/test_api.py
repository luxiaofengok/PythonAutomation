import pytest
from utils.api_helper import APIHelper
from utils.config_reader import ConfigReader


class TestJSONPlaceholderAPI:
   
    def test_get_todo_verify_id_1(self, api):

        # Call API to get todo with id=1
        todo = api.get("todos/1")
        
        print(f"\n📋 Todo response: {todo}")

        
        # Assertions
        assert todo["userId"] == 1, \
            f"Expected userId=1 but got {todo['userId']}"
        
        assert todo["id"] == 1, \
            f"Expected id=1 but got {todo['id']}"
        
        assert todo["title"] == "delectus aut autem", \
            f"Expected title='delectus aut autem' but got '{todo['title']}'"
        
        assert todo["completed"] == False, \
            f"Expected completed=False but got {todo['completed']}"
        # Print success
        print(f"\n✅ Verified todo:")
        print(f"   User ID: {todo['userId']}")
        print(f"   ID: {todo['id']}")
        print(f"   Title: {todo['title']}")
        print(f"   Completed: {todo['completed']}")
    @pytest.mark.api
    def test_get_user_verify_id_2(self, api):
     
        # Call API to get user with id=2
        user = api.get("users/2")
        
        print(f"\n👤 User response: {user}")
        
        # Assertions
        assert user["name"] == "Ervin Howell", \
            f"Expected name='Ervin Howell' but got '{user['name']}'"
        
        assert user["username"] == "Antonette", \
            f"Expected username='Antonette' but got '{user['username']}'"
        
        assert user["email"] == "Shanna@melissa.tv", \
            f"Expected email='Shanna@melissa.tv' but got '{user['email']}'"

        
        # Print success
        print(f"\n✅ Verified user:")
        print(f"   Name: {user['name']}")
        print(f"   Username: {user['username']}")
        print(f"   Email: {user['email']}")
