from flask import Flask

app = Flask(__name__)
app.secret_key = "No, you can't borrow my pen"