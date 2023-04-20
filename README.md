# Tira Huggingface Measure Evaluator

This repository contains a general evaluator for the tira shared task framework based on the Huggingface [evaluate](https://huggingface.co/docs/evaluate/main/en/index) library.

## Usage

Measure accuracy, precision, recall and f1.

```sh
tira-run \
    --input-run $PWD/tira-test/csv/test-predictions \
    --input-directory $PWD/tira-test/csv/test-references \
    --image webis/tira-hf-evaulator:0.0.1 \
    --command '/evaluation.py --metrics accuracy precision recall f1 --predictions $inputRun/predictions.txt --references $inputDataset/references.txt --data-format csv --output-prototext $outputDir/evaluation.prototext'
```

This produces outputs in `tira-output/evaluation.prototext` like:

```prototext
measure{
  key: "Accuracy"
  value: "0.47330960854092524"
}
measure{
  key: "Precision"
  value: "0.47268408551068886"
}
measure{
  key: "Recall"
  value: "0.47268408551068886"
}
measure{
  key: "F1"
  value: "0.47268408551068886"
}
```

Evaluate NER using seqeval

```sh
tira-run \
    --input-run $PWD/tira-test/iob/test-predictions \
    --input-directory $PWD/tira-test/iob/test-references \
    --image webis/tira-hf-evaulator:0.0.1 \
    --command '/evaluation.py --metrics seqeval --predictions $inputRun/predictions.txt --references $inputDataset/references.txt --data-format IOB1 --output-prototext $outputDir/evaluation.prototext'
```

## Installation + deployment

`make build-docker`

## Tests

`pytest test`
