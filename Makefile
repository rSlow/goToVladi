start:
	docker compose up --build -d

stop:
	docker compose down --remove-orphans

update: stop pull start

pull:
	git pull
