
import os

from finae import ask_llm, init_cache
from mountain import Mountain

dir_path = os.path.dirname(os.path.realpath(__file__))

def get_mountains():
    prompt = """List top 50 mountains in the world. Each line is a mountain, include altitude in meters and feet."""
    output = ask_llm(prompt)
    lines = output.split('\n')
    results = []
    for line in lines:
        try:
            o = Mountain(line)
            s = str(o)
            results.append(o)
        except:
            pass
    return results


if __name__ == '__main__':
    init_cache(dir_path)
    mountains = get_mountains()
    for m in mountains:
        print(m)
