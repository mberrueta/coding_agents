import unittest
from unittest.mock import MagicMock, patch, mock_open

from cli.agents.task import TaskAgent
from cli.core.context_bundle import ContextBundle


class TestTaskAgent(unittest.TestCase):
    def setUp(self):
        self.console = MagicMock()
        self.agent = TaskAgent(console=self.console)
        self.agent.llm = MagicMock()

    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_generate_creates_tasks_and_output_dir(self, mock_makedirs, mock_exists):
        # Arrange
        context = ContextBundle(user_instructions="Some user instructions", context="Some user context")
        kwargs = {
            "requirement_path": "dummy_req.md",
            "design_path": "dummy_design.md",
            "output_dir": "dummy_output"
        }

        # First call: output dir does not exist
        mock_exists.return_value = False
        
        llm_response = MagicMock()
        llm_response.content = """
### Task: Task 1
**Related Requirement:** FR-1
**Description:** Desc 1
**Files to be Modified/Created:** - file1.txt
**Acceptance Criteria (for TDD):** - AC1
**Technical Guidance:** Guide 1
---[TASK]---
### Task: Task 2
**Related Requirement:** FR-2
**Description:** Desc 2
**Files to be Modified/Created:** - file2.txt
**Acceptance Criteria (for TDD):** - AC2
**Technical Guidance:** Guide 2
        """
        self.agent.llm.invoke.return_value = llm_response

        # Act
        mock_file_content = {
            "dummy_req.md": "Requirement content",
            "dummy_design.md": "Design content"
        }
        
        original_open = open

        def custom_open(filename, *args, **kwargs):
            if filename == self.agent.template_path:
                return original_open(filename, *args, **kwargs)
            if filename in mock_file_content:
                return mock_open(read_data=mock_file_content[filename])(*args, **kwargs)
            # For any other file (i.e. output files), return a simple mock
            return mock_open()(*args, **kwargs)

        with patch("builtins.open", side_effect=custom_open):
            # First call
            self.agent.generate(context, **kwargs)
            # Second call
            mock_exists.return_value = True
            result = self.agent.generate(context, **kwargs)

        # Assert
        self.assertEqual(self.agent.llm.invoke.call_count, 2)
        self.assertEqual(result, "Tasks saved to dummy_output")
        
        mock_makedirs.assert_called_once_with("dummy_output")


if __name__ == "__main__":
    unittest.main()
