# docker build -t webis/tira-hf-evaulator:0.0.3 .
FROM python:3.10

RUN pip3 install evaluate scikit-learn seqeval
RUN python3 -c 'import evaluate; evaluate.load("accuracy"); evaluate.load("recall"); evaluate.load("precision"); evaluate.load("f1"); evaluate.load("seqeval"); evaluate.load("matthews_correlation"); evaluate.load("fschlatt/ner_eval")'

COPY evaluation.py /evaluation.py
ENV OFFLINE=True

ENTRYPOINT [ "/evaluation.py" ]
