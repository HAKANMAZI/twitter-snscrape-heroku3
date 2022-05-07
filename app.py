# pip install flask
# pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git
# pip install pandas

from flask import Flask, render_template, request, url_for, redirect, send_file, session
import snscrape.modules.twitter as twitter
import pandas as pd
import os 

posts = []

def delete_csv():
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".csv"):
            print(item)
            os.remove(os.path.join(dir_name, item))


from datetime import datetime
from datetime import timedelta
class most_liked_tweets():
    def __init__(self) -> None:
        self.yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        self.tomorrow = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')

    def post_times(self):
        times = {
            "yesterday" : self.yesterday,
            "tomorrow" : self.tomorrow
        }
        post_times.append(times)
        return post_times


    def trending_tweets_url(self, keyword, like_count=50, sincetime="", untiltime=""):
        counter = 0
        for i, tweet in enumerate(twitter.TwitterSearchScraper(keyword + ' since:'+sincetime+' until:'+untiltime).get_items()):
            if tweet.likeCount > like_count:
                if counter == 5: break
                print(self.yesterday)
                print(self.tomorrow)
                print(tweet.url)

                tweet = {
                'username': tweet.user.username,
                'content': tweet.content,
                'date_posted': tweet.date,
                'url': tweet.url
                }
                posts.append(tweet)
                counter +=1


cls=most_liked_tweets()
post_times = []
post_times = cls.post_times()


app = Flask(__name__)
app.config['SECRET_KEY'] = "DemoString"

@app.route("/", methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET','POST'])
def login():
    return render_template("index.html")

@app.route("/register", methods=['GET','POST'])
def register():
    return render_template("index.html")



@app.route("/home", methods=['GET','POST'])
def home():
    delete_csv()
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['keyword'] = request.form.get('keyword')
        session['sincetime'] = request.form.get('sincetime')
        session['untiltime'] = request.form.get('untiltime')
        session['retweetcount'] = request.form.get('retweetcount')

        session['username3'] = request.form.get('username3')
        session['retweetcount3'] = request.form.get('retweetcount3')

        session['keyword4'] = request.form.get('keyword4')
        session['retweetcount4'] = request.form.get('retweetcount4')

        
        if request.form['btn'] == 'Process1':
            if session['username']:
                print("Process1")
                userTweets_CSV(session['username'], session['sincetime'], session['untiltime'])
                return send_file(os.path.abspath(session['username']+'.csv'), as_attachment=True)
  
        if request.form['btn'] == 'Process2':
            if session['keyword']:
                print("Process2")
                keyword_CSV(session['keyword'], session['sincetime'], session['untiltime'])
                return send_file(os.path.abspath(session['keyword']+'.csv'), as_attachment=True) 

        if request.form['btn'] == 'Process3':
            if session['username3']:
                print("Process3")
                retweetcount_CSV(session['username3'],  int(session['retweetcount3']), session['sincetime'], session['untiltime'])
                return send_file(os.path.abspath(session['username3']+'.csv'), as_attachment=True)


        if request.form['btn'] == 'Process4':   
            if session['keyword4']:
                print("Process4")
                keywordretweet_CSV(session['keyword4'],  int(session['retweetcount4']), session['sincetime'], session['untiltime'])
                return send_file(os.path.abspath(session['keyword4']+'.csv'), as_attachment=True)


    return render_template("home.html")




@app.route("/trending_tweets_url", methods=['GET','POST'])
def trending_tweets_url():
    delete_csv()
    if request.method == 'POST':
        session['keyword'] = request.form.get('keyword')
        session['like_count'] = request.form.get('like_count')
        session['sincetime'] = request.form.get('sincetime')
        session['untiltime'] = request.form.get('untiltime')

        if session['keyword']:
            cls.trending_tweets_url(session['keyword'], int(session['like_count']), session['sincetime'], session['untiltime'] )

    print(post_times)    
    return render_template('trending_tweets_url.html', post_times=post_times, posts = posts)
    

if __name__=="__main__":
    app.run(debug=True)
