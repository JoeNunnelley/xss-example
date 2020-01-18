import html
import os
import random
import base64

from flask import Flask, request, session
from model import Message 

app = Flask(__name__)
app.secret_key = b'_i67#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'csrf_token' not in session:
      session['csrf_token'] = str(random.randint(1000000, 9999999))

    if request.method == 'POST':
        if request.form.get('csrf_token', None) == session['csrf_token']:
          m = Message(content=request.form['content'])
          m.save()

    body = """
<html>
<body>
<h1>Class Message Board</h1>
<h2>Contribute to the Knowledge of Others</h2>
<form method="POST">
    <textarea name="content"></textarea>
    <input type="submit" value="Submit">
    <input type="hidden" name="csrf_token" value="{}">
</form>

<h2>Wisdom From Your Fellow Classmates</h2>
""".format(session['csrf_token'])
    
    for m in Message.select():
        body += """
<div class="message">
{}
</div>
""".format(html.escape(m.content))

    return body 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

