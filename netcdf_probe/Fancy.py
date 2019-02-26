class Fancy:
    """
    Helper class to call DoubleBufferedCache.load() with fancy indexing
        - usage : yourArray(Fancy()[fancy_indexes])
        - Introduce overhead, mosly for convenient testing.
    """
    def __getitem__(self, keys):
        return keys

