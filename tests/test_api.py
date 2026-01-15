import pytest
from utils.api_helper import APIHelper
from utils.config_reader import ConfigReader


class TestJSONPlaceholderAPI:
    """Test cases for JSONPlaceholder API"""

    @pytest.fixture
    def api(self):
        """Create API helper with config"""
        config = ConfigReader("testsetting.json")
        helper = APIHelper(base_url=config.get("api_url"))
        yield helper
        helper.close()
    
    def test_get_todo_verify_id_1(self, api):
        """
        Test: Call GET https://jsonplaceholder.typicode.com/todos/1
        Verify:
          - userId = 1
          - id = 1
          - title = "delectus aut autem"
          - completed = false
        """
        # Call API to get todo with id=1
        response = api.get("todos/1")
        
        # Verify status code
        assert response.status_code == 200, \
            f"Expected 200 but got {response.status_code}"
        
        # Parse JSON response
        todo = response.json()
        
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
