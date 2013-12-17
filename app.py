from flask import Flask, render_template, request, Response, session, abort, jsonify, url_for
from twilio.rest import TwilioRestClient
import json
import requests as REQ

app = Flask(__name__)
app.config['DEBUG'] = True


# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC5bba681cd20ff9c94e958307f2d32482"
auth_token  = "d6fdd4e686221130e3022366c4804594"
client = TwilioRestClient(account_sid, auth_token)

@app.route('/search')
def index():
  phone_no = request.args.get('From')
  body = request.args.get('Body')
  artist_url = "http://api.jambase.com/artists"
  events_url = "http://api.jambase.com/events"
  artist_args = {"page":0, "api_key":"FYNKUZA76VXDNHM5GH3EVE3R","name": body}
  r = REQ.get(artist_url, params=artist_args)
  if not r.json()['Artists']:
    return Response(render_template('noartist.xml', mimetype='text/xml'))
  artist_id = r.json()['Artists'][0]['Id']
  events_args = {"page":0, "api_key":"FYNKUZA76VXDNHM5GH3EVE3R", "zipCode":"94114", "radius":"50"}
  print "artist id: "+str(artist_id)
  events_args['artistId'] = artist_id
  s = REQ.get(events_url, params=events_args).json()
  if not s['Events']:
    return Response(render_template('noevents.xml', mimetype='text/xml'))
  print "events url: "+events_url+" events args: "+ str(events_args) + " response: "+ str(s)
  return Response(render_template('results.xml', mimetype='text/xml', events = s, phone_no = phone_no ))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)
