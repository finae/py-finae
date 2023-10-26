from finae import Extraction
from mountain import Mountain

if __name__ == '__main__':
    extraction = Extraction('List top 5 mountains in the world.', [Mountain])
    extraction.extract(rounds=3)
