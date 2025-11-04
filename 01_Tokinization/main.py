import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
text = "Hey There! My name is Manidhar Karnatakam"

tokens=enc.encode(text)
print('Tokens : ',tokens) # [25216, 3274, 0, 3673, 1308, 382, 3265, 315, 8665, 80010, 266, 34093]
print("No of tokens(GPT-4o) : ",len(tokens))

decoded=enc.decode(tokens)
print('Decoded Text : ',decoded) # Hey There! My name is Manidhar Karnatakam
