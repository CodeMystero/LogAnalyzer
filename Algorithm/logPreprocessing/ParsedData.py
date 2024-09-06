class ParsedData:
    def __init__(self, timestamp = None, data = None):
        self.timestamp = timestamp
        self.data = data

    def __repr__(self):
        return f"ParsedData(timestamp={self.timestamp}, data={self.data})"
    
    def to_dict(self):
        """Returns the object as a dictionary."""
        return {
            "timestamp": self.timestamp,
            "data": self.data
        }

    def update(self, timestamp=None, data=None):
        """Update both timestamp and data."""
        if timestamp is not None:
            self.timestamp = timestamp
        if data is not None:
            self.data = data
