from flask import Flask
from threading import Thread

app = Flask('')

@app.route("/")
def home():
  return '''
        Help: prefix "e-" |
              load cogs "lc -name-" |
              unload cogs "uc -name-" |
              ping "ping" |
              kick "kick -mention-" |
              ban "ban -mention-" |
              unban "unban -mention- (or User ID)" |
              8ball "8ball -question-" |
              avatar competition "ac (name)"
        '''

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()