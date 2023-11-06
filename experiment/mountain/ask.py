from finae import init_cache
from mountain import Mountain

if __name__ == '__main__':
    init_cache()
    mountains = Mountain.__finae_query_llm__('List top 50 mountains in the world.')
    for m in mountains:
        print(m)
