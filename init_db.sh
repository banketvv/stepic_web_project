#!/usr/bin/env bash
mysql -uroot -e "create database ask"
mysql -uroot -e "create user ask identified by '<YJGYZ'"
mysql -uroot -e "grant all on ask.* to ask"
python ask/manage.py makemigrations
python ask/manage.py migrate
cd ask
sudo chmod 666 db.sqlite3
sudo chmod -R 777 .