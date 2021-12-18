FROM imjeffhi4/syllable_model

WORKDIR /app

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "syllables:app", "--host", "0.0.0.0", "--port", "8000"]