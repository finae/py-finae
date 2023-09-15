from finae import query_llm, init_cache
from mountain import Mountain

if __name__ == '__main__':
    init_cache()
    mountains = query_llm('List top 50 mountains in the world.', Mountain)
    for m in mountains:
        print(m)
