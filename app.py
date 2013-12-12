from flask import Flask, render_template, request, Response, session, abort, jsonify, url_for
from twilio.rest import TwilioRestClient
import json

app = Flask(__name__)
app.config['DEBUG'] = True


# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC5bba681cd20ff9c94e958307f2d32482"
auth_token  = "d6fdd4e686221130e3022366c4804594"
client = TwilioRestClient(account_sid, auth_token)

@app.route('/search')
def index():
  return Response(render_template('say.xml', mimetype='text/xml', phone_no=request.args.get('From'), body=request.args.get('Body') ))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)
