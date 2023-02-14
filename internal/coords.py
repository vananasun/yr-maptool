
class Coords:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return '(x: {}, y: {})'.format(self.x, self.y)


    @staticmethod
    def from_txt(coords_txt: str) -> "Coords":
        num = int(coords_txt)
        # @NOTE: With NewIniFormat lower than 4 it's 128 not 1000
        y = num // 1000 # coefficient is 1000 in Red Alert 2 and TS
        x = num % 1000
        return Coords(x, y)


    @staticmethod
    def to_txt(coords: "Coords") -> str:
        return str(coords.y * 1000 + coords.x)