from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from fastapi import FastAPI
import re
from pydantic import BaseModel
import torch
from string import punctuation
import logging
logging.getLogger('transformers').setLevel(logging.CRITICAL)

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
syl_path = "./Model"
syl_model = GPTNeoForCausalLM.from_pretrained(syl_path).to(device)
syl_tokenizer = GPT2Tokenizer.from_pretrained(syl_path)

class UserInput(BaseModel):
    txt: str

@app.post('/syllables/')
async def main(x: UserInput):
    return generate_syllables(x.txt.lower())

def get_formatted_output(output):
    syllables_string = re.findall('<SYLLABLES> (.+?)<\|endoftext\|>', output)
    if syllables_string:
        return syllables_string[0].strip().split()
    else:
        return None
def generate_syllables(txt):
    txt = txt.replace('-', ' ')
    txt = re.sub(f'[{punctuation}]', '', txt)
    words = txt.split()
    syllables = []
    for word in words:
        syllables.extend(generate_output(word))
    return syllables

def generate_output(word):
    split_word = " ".join(word)
    input_string = f"{word} <SPELLED> {split_word} <SYLLABLES>"
    tokenized_input =syl_tokenizer.encode(input_string, return_tensors='pt').to(device)
    output = syl_model.generate(tokenized_input, max_length=150)[0]
    decoded_output = syl_tokenizer.decode(output)
    return  get_formatted_output(decoded_output)

