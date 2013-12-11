from flask import Flask, render_template, request, Response, session, abort, jsonify, url_for
from twilio.rest import TwilioRestClient
import json
import redis
import re
import base64

app = Flask(__name__)
app.config['DEBUG'] = True

r = redis.StrictRedis(host='localhost',port=6379,db=0)

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC2dd3b641addfcbf5e5cc2af60a03fb73"
auth_token  = "041d85969d3e7df0ba2046ea977a825e"
client = TwilioRestClient(account_sid, auth_token)

@app.route('/twipic')
def index():
    return render_template('picture.html') 

@app.route('/send',methods=['POST'])
def send():
  dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
  imgData = request.form.get('base64img')
  imgData = dataUrlPattern.match(imgData).group(2)
  ph = request.form.get('phone')
  print "request phone: "+ph
  code = request.form.get('code')
  print "request code: "+code
  print "from redis: "+r.get(ph)
  if r.get(ph) == code:
    fh = open("static/"+str(ph)+".png", "wb")
    fh.write(base64.b64decode(imgData))
    fh.close()
    #send MMS
    print "url: "+url_for('static',filename=str(ph)+'.png',_external=True)
    imgur = url_for('static',filename=str(ph)+'.png',_external=True)
    #sms = client.sms.messages.create(media_url=url_for('static',filename=str(ph)+'.png',_external=True),
    #sms = client.sms.messages.create(media_url="http://eofdreams.com/data_images/dreams/cat/cat-06.jpg",
    #to=ph,
    #from_="+19252320999")
    message = client.messages.create(body="Jenny please?! I love you <3",
    to=ph,
    from_="+19252320999",
    media_url=imgur)
    return json.dumps({'success':True}) 
  return json.dumps({'success':False}) 

@app.route('/text',methods=['POST'])
def text():
  id = r.incr('sessionid')
  print "form: "+str(request.form)
  ph = request.form.get('phone')  
  r.set(ph,id)
  sms = client.sms.messages.create(body="Enter the following code on the site:"+str(id),
    to=ph,
    from_="+19252320999")
  return jsonify({'phone':ph}) 

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)
