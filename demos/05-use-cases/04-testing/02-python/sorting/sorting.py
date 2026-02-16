class ObjectSorter:
    def __init__(self, objects):
        self.objects = objects

    def sort(self, field, ascending=True):
        self.objects.sort(key=lambda obj: obj[field], reverse=not ascending)
        return self.objects
