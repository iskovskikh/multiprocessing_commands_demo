

ifeq (,$(wildcard ./.env))
    $(error .env file not found. Please create one.)
endif

include .env
export

.PHONY: local
local:
	python ./app/main.py

