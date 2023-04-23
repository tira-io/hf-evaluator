build-docker:
	docker build -t webis/tira-hf-evaulator:0.0.2 hf_evaluator
	docker push webis/tira-hf-evaulator:0.0.2

