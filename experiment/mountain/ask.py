from finae import init_cache
from mountain import Mountain

if __name__ == '__main__':
    init_cache()
    mountains = Mountain.query_llm('List top 50 mountains in the world.')
    for m in mountains:
        print(m)
