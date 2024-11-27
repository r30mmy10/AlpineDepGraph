import unittest
from unittest.mock import patch
from dependency_visualizer import get_dependencies, generate_mermaid


class TestDependencyVisualizer(unittest.TestCase):
    @patch('subprocess.run')
    def test_get_dependencies(self, mock_subprocess_run):
        # Имитируем вывод команды 'apk info -R'
        mock_subprocess_run.return_value.stdout = (
            "fake-package depends on:\n"
            "    dependency1\n"
            "    dependency2\n"
        )

        dependencies = get_dependencies("fake-package", 1)
        self.assertEqual(dependencies, ["dependency1", "dependency2"])

    def test_generate_mermaid(self):
        # Тестируем генерацию mermaid кода
        dependencies = ["libc", "busybox"]
        mermaid_code = generate_mermaid("alpine-baselayout", dependencies)
        self.assertIn("alpine-baselayout --> libc", mermaid_code)
        self.assertIn("alpine-baselayout --> busybox", mermaid_code)


if __name__ == '__main__':
    unittest.main()


