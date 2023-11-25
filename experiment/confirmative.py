from finae import ask_llm


output = ask_llm('''
Answer: Yes, red is a color. It is one of the primary colors and is often associated with emotions such as love, passion, and anger.
                 
Is it a confirmative answer or not?
''')

print(output)
