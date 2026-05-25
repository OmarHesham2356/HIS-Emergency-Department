MYSQL_HOST ?= 127.0.0.1
MYSQL_PASS ?= April2005
MYSQL := mysql -h $(MYSQL_HOST) -u root -p$(MYSQL_PASS)

.PHONY: run seed reset lint

run:
	streamlit run app/app.py

seed:
	PYTHONPATH=app python3 sql/seed_data.py

reset:
	$(MYSQL) < sql/reset.sql

reset-full:
	$(MYSQL) < sql/reset.sql
	$(MYSQL) < sql/merge/full_schema.sql
	PYTHONPATH=app python3 sql/seed_data.py
