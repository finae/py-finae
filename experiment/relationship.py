from finae import ask_llm

output = ask_llm('''Given Tom is mother of Jack, Jack is father of Zack.
                 
What is the gender of Zack?
''')

print(output)
