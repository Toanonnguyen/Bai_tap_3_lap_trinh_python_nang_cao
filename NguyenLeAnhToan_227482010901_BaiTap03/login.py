import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, session

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='student',
            user='postgres',
            password='toanon2004',
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as e:
        print(f"Không thể kết nối với dữ liệu: {e}")
        return None

def authenticate(username, password):
    valid_username = "Toanon"
    valid_password = "123456"
    return username == valid_username and password == valid_password
