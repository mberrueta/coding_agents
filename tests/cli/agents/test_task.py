import unittest
from unittest.mock import MagicMock, patch
import os

from cli.agents.task import TaskAgent
from cli.core.context_bundle import ContextBundle


class TestTaskAgent(unittest.TestCase):
    def setUp(self):
        self.console = MagicMock()
        self.agent = TaskAgent(console=self.console)
        self.agent.llm = MagicMock()

    @patch("builtins.open")
    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_generate_creates_tasks(self, mock_makedirs, mock_exists, mock_open):
        # Arrange
        context = ContextBundle(user_instructions="Some user instructions", context="Some user context")
        kwargs = {
            "requirement_path": "dummy_req.md",
            "design_path": "dummy_design.md",
            "output_dir": "dummy_output"
        }

        mock_exists.return_value = True
        # Mock reading requirement and design files
        mock_open.side_effect = [
            unittest.mock.mock_open(read_data="Requirement content").return_value,
            unittest.mock.mock_open(read_data="Design content").return_value,
            unittest.mock.mock_open().return_value, # for task1.md
            unittest.mock.mock_open().return_value  # for task2.md
        ]

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
        result = self.agent.generate(context, **kwargs)

        # Assert
        self.agent.llm.invoke.assert_called_once()
        self.assertEqual(result, "Tasks saved to dummy_output")
        
        # Check that files were written
        self.assertEqual(mock_open.call_count, 4) # req, design, task1, task2
        
        # Check if output dir was created if not exists
        mock_exists.return_value = False
        mock_open.reset_mock()
        mock_open.side_effect = [
            unittest.mock.mock_open(read_data="Requirement content").return_value,
            unittest.mock.mock_open(read_data="Design content").return_value,
            unittest.mock.mock_open().return_value, # for task1.md
            unittest.mock.mock_open().return_value  # for task2.md
        ]
        self.agent.generate(context, **kwargs)
        mock_makedirs.assert_called_with("dummy_output")


if __name__ == "__main__":
    unittest.main()