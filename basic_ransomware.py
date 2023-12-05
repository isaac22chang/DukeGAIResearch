import os
import platform
import openai
import subprocess
from dotenv import load_dotenv
load_dotenv()


def install_libraries(library_string):
    libraries = library_string.split(",")

    for library in libraries:
        try:
            subprocess.check_call(['pip', 'install', library])
            print(f'Successfully installed {library}')
        except subprocess.CalledProcessError as e:
            print(f'Error installing {library}: {e}')


client = openai.OpenAI(
        api_key = os.getenv('OPENAI_API_KEY'),
)

messages = [ {"role": "system", "content": "Please respond to the best of your ability. If my prompt begins with 'Mode: Code' you should ONLY print out code and nothing else. For instance, if my prompt asked 'Mode:Code How do I print out hello in Python?' You should only respond with 'print(Hello World)' and nothing else. "}]

message1 = "Mode: Code. REMINDER THAT MODE CODE MEANS NOTHING EXCEPT CODE, the response you give will be run in an IDE. Assume no libraries are downloaded except OS. Create a program that encrypts all files and directories in the current directory and encrypt it with AES encryption. If you create a new encrypted file, remember to delete the old one. Store the AES key in a separate txt file named keys.txt. Before the import statements such as 'import os', have a comment that's ONLY content are the names of the Python libraries, needed for the script in one line. The format for this would be - first line: '# cryptography, warnings'. second part: -the actual code for the rest of the script. I will go mad if you put this in a comment again."

messages.append({"role": "user", "content": message1})


chat = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
)


reply = chat.choices[0].message.content
print(f"ChatGPT: {reply}")




filename = 'g.py'

with open(filename, 'w') as f:
    f.write(reply)

with open('g.py') as f:
    first_line = f.readline().strip()
    print("fL:", first_line)

install_libraries(first_line)
    
print("went thru")
subprocess.run(["python", filename])

