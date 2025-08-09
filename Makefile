.PHONY: up down logs initdb

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

initdb:
	# Run SQL schema
	docker compose run --rm backend bash -c "psql $${DATABASE_URL} -f app/models.sql"