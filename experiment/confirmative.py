from finae import ask_llm

output = ask_llm('''
Answer: Yes, red is a color. It is one of the primary colors and is often associated with emotions such as love, passion, and anger.
                 
Is it a positive or negative answer? Can you give one word?
''')

print(output)


output = ask_llm('''
No, Aconcagua is not in Europe.

Aconcagua is the highest mountain in the Americas and the highest peak outside Asia. It is located in the Andes mountain range, in Argentina, South America. Europe, on the other hand, is a continent located to the north and east of the Atlantic Ocean, and is separated from South America by the Southeast Atlantic Ocean. Therefore, Aconcagua is not in Europe.
                 
Is it a positive or negative answer? Can you give one word?
''')

print(output)
