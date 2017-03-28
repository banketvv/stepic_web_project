#!/usr/bin/env bash
mysql -uroot -e "create database ask"
mysql -uroot -p -e "create user ask identified by '<YJGYZ'"
mysql -uroot -p -e "grant all on ask.* to ask"