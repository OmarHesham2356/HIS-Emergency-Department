.PHONY: run seed reset lint

run:
	nix develop --command streamlit run app/app.py

seed:
	nix develop --command bash -c 'PYTHONPATH=app python3 sql/seed_data.py'

reset:
	mysql -u root -pApril2005 < sql/reset.sql

reset-full:
	mysql -u root -pApril2005 < sql/reset.sql
	mysql -u root -pApril2005 < sql/merge/full_schema.sql
	nix develop --command bash -c 'PYTHONPATH=app python3 sql/seed_data.py'
