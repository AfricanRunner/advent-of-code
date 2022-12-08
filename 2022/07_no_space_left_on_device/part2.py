import re
import sys
from dataclasses import dataclass


@dataclass
class File:
    name: str
    size: int


class Directory:

    def __init__(self, name: str, parent: 'Directory | None'):
        self._name = name
        self._files = {}
        self._parent = parent
        self._sub_directories = {}
        self._size = 0

    def get_name(self) -> str:
        return self._name

    def get_parent(self) -> 'Directory | None':
        return self._parent

    def add_file(self, file: File):
        self._files[file.name] = file

    def add_directory(self, name: str):
        self._sub_directories[name] = Directory(name, self)

    def get_sub_directory(self, directory_name: str) -> 'Directory | None':
        if directory_name not in self._sub_directories:
            return None
        return self._sub_directories[directory_name]

    def calculate_size(self):
        for sub_directory in self._sub_directories.values():
            sub_directory.calculate_size()
        self._size = sum([
            sub_directory.get_size()
            for sub_directory in self._sub_directories.values()
        ])
        self._size += sum([file.size for file in self._files.values()])

    def get_size(self) -> int:
        return self._size

    def find_smallest_ge(self, n: int) -> int | None:
        if not self._sub_directories:
            return self._size if self._size >= n else None
        candidates = [sub_directory.find_smallest_ge(n)
                      for sub_directory in self._sub_directories.values()]
        candidates = [candidate for candidate in candidates
                      if candidate is not None]
        if len(candidates) == 0:
            return self._size if self._size >= n else None
        return min(candidates)


class Terminal:

    def __init__(self, root: Directory):
        self._root = root
        self._current_directory = root

    def go_to_dir(self, name: str):
        if directory := self._current_directory.get_sub_directory(name):
            self._current_directory = directory
        else:
            raise RuntimeError(f'{name} is not a directory '
                               f'of {self._current_directory.get_name()}')

    def add_file(self, file: File):
        self._current_directory.add_file(file)

    def add_directory(self, name: str):
        self._current_directory.add_directory(name)

    def go_back(self):
        parent = self._current_directory.get_parent()
        if parent is None:
            raise RuntimeError(
                f'Directory {self._current_directory.get_name()} '
                'doesn\'t have a parent')
        self._current_directory = parent

    def process(self, command: str):
        if match := re.match('^\\$ cd \\.\\.$', command):
            self.go_back()
        elif match := re.match('^\\$ cd (\\S+)$', command):
            directory_name = match.group(1)
            self.go_to_dir(directory_name)
        elif match := re.match('^(\\d+) (\\S+)$', command):
            size = match.group(1)
            name = match.group(2)
            self.add_file(File(name, int(size)))
        elif match := re.match('^dir (\\S+)$', command):
            directory_name = match.group(1)
            self.add_directory(directory_name)
        elif re.match('^\\$ ls$', command):
            return
        else:
            raise RuntimeError(f'Invalid command {command}')


def main(input: list[str]):
    root = Directory('/', None)
    terminal = Terminal(root)
    for command in input[1:]:
        terminal.process(command)
    root.calculate_size()
    root_size = root.get_size()
    needed_space = 30_000_000 - (70_000_000 - root_size)
    print(root.find_smallest_ge(needed_space))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
