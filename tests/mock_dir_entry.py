class MockDirEntry:
    """mocks a DirEntry object"""
    def __init__(self, path):
        self.path = path
        if path[-1] == '/':
            self.isdir = True
            self.name = path.split('/')[-2]
        else:
            self.isdir = False
            self.name = path.split('/')[-1]
            
    def is_dir(self):
        return self.isdir

    @staticmethod
    def make(items):
        """Factory method to create tuples of MockDirEntry
        similar to what os.scandir() would return"""
        files = []
        for item in items:
            files.append(MockDirEntry(item))
        return files
