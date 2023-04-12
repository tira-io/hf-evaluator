# Tira Huggingface Measure Evaluator

This repository contains a general evaluator for the tira shared task framework based on the Huggingface [evaluate](https://huggingface.co/docs/evaluate/main/en/index) library.

## Installation

`cd hf_evaluator && docker build -t hf-evaulator .`

## Usage

Measure accuracy, precision, recall and f1.

```cd tira-test/csv/ && tira-run --input-run $PWD/test-predictions --input-directory $PWD/test-references --image hf-evaluator --command '/evaluation.py --metrics accuracy precision recall f1 --predictions $inputRun/predictions.txt --references $inputDataset/references.txt --data-format csv --output-prototext $outputDir/evaluation.prototext'```

Evaluate NER using seqeval

```cd tira-test/iob/ && tira-run --input-run $PWD/test-predictions --input-directory $PWD/test-references --image hf-evaluator --command '/evaluation.py --metrics seqeval --predictions $inputRun/predictions.txt --references $inputDataset/references.txt --data-format IOB1 --output-prototext $outputDir/evaluation.prototext'```

## Tests

`pytest test`
