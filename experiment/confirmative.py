from finae import ask_llm

output = ask_llm('''
Answer: Yes, red is a color. It is one of the primary colors and is often associated with emotions such as love, passion, and anger.
                 
Is it a confirmative answer or not?
''')

print(output)


output = ask_llm('''
Answer: Yes, it is a confirmative answer. It is a statement that affirms that red is a color.
                 
Is it a confirmative answer or not?
''')

print(output)
