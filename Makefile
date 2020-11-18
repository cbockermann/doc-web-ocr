VERSION=v1

docker:
	docker build -t doc-web-ocr:$(VERSION) .
