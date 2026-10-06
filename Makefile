install:
	python3 -m pip install -r requirements.txt

run:
	python3 app.py

test:
	python3 -m unittest discover -s tests -v

docker-up:
	docker compose up --build

docker-down:
	docker compose down
