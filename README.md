# Syllabizer Service

Uses a fine-tuned version of GPT Neo to decompose words into a list of syllables. This repository offers a docker-based service with FastAPI as a backend. The model is also available on HuggingFace [here](https://huggingface.co/imjeffhi/syllables_generator). 

# How to Run

To build the docker image, run the following:

```docker
docker build --no-cache -t syllables .
```

You can then start the API with the following:

```docker
docker run -p 8000:8000 syllables
```

# Using the API

To use the API, make a POST request to “[http://127.0.0.1:8000/syllables/](http://127.0.0.1:8000/syllables/)” with the string of text you wish to use. The model is primarily trained on single word inputs, but the API automatically splits sentences into individual words if you have longer inputs. Below is an example call

```python
txt = 'Syllable generator'
items= {"txt": txt}
x = requests.post('http://127.0.0.1:8000/syllables/', json=items)
json.loads(x.content)
```

Results:

```python
['syl', 'la', 'ble', 'gen', 'er', 'a', 'tor']
```
