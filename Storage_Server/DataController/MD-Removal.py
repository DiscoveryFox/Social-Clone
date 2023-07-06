from exif import Image


class ImageObj:
    def __init__(self, path: str):
        self.path = path
        self.image = Image(path)

    def remove_metadata(self):
        for i in sorted(self.image.list_all()):
            self.image.delete(i)


paths = '/home/robbie-simmonds/Desktop/testing.jpg'
test = ImageObj(path=paths)
for f in sorted(test.image.list_all()):
    print(str(f) + " " + str(test.image.get(f)))

print()

test.remove_metadata()
for f in sorted(test.image.list_all()):
    print(str(f) + " " + str(test.image.get(f)))
