import os
import unittest
from unittest.mock import patch
from io import StringIO
from DirectoryTreePrinter import print_tree, IGNORE_SET

class TestDirectoryTreePrinter(unittest.TestCase):
    def setUp(self):
        # Crée une structure de répertoires de test
        self.test_dir = 'test_project'
        os.makedirs(os.path.join(self.test_dir, 'dir1', 'subdir1'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'dir2'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, '.git'), exist_ok=True) # Devrait être ignoré

        # Crée des fichiers de test
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write('hello')
        with open(os.path.join(self.test_dir, 'dir1', 'file2.py'), 'w') as f:
            f.write('print("hello")')
        with open(os.path.join(self.test_dir, 'dir1', 'subdir1', 'file3.log'), 'w') as f:
            f.write('log entry')
        with open(os.path.join(self.test_dir, 'dir2', 'file4.tmp'), 'w') as f:
            f.write('temp file')

    def tearDown(self):
        # Nettoie la structure de répertoires de test
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_print_tree_output(self):
        # Redirige la sortie standard pour la capturer
        with patch('sys.stdout', new=StringIO()) as fake_out:
            print_tree(self.test_dir)
            output = fake_out.getvalue().strip()

        # Crée la sortie attendue
        expected_output = (
            "├── dir1/\n"
            "│   ├── file2.py\n"
            "│   └── subdir1/\n"
            "│       └── file3.log\n"
            "├── dir2/\n"
            "│   └── file4.tmp\n"
            "└── file1.txt"
        )
        
        # Supprime les espaces de fin de chaque ligne pour une comparaison robuste
        output_lines = [line.rstrip() for line in output.splitlines()]
        expected_lines = [line.rstrip() for line in expected_output.splitlines()]

        self.assertEqual(output_lines, expected_lines)

    def test_ignore_git_directory(self):
        # Vérifie que le répertoire .git est bien ignoré
        with patch('sys.stdout', new=StringIO()) as fake_out:
            print_tree(self.test_dir)
            output = fake_out.getvalue()
            self.assertNotIn('.git', output)

if __name__ == '__main__':
    unittest.main()
