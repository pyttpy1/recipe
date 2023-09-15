from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '99ae87899eb62b3f2eded6c18e220f7a1e99a8d3688351317e8cb3803ca5dc20'