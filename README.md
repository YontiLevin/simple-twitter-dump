# Simple Twitter Dump  

<p align="center">
  <img src="imgs/opera_meme.jpg" width="350" alt="Everyone gets a tweets!"/>
</p>

As simple as possible 
---
1. Twitter signup & Installation
    1. Get yourself a Twitter account and create a Twitter app.
        - [create account](https://help.twitter.com/en/create-twitter-account)  
        - [create app](http://docs.inboundnow.com/guide/create-twitter-application/)
    
    2. Save [twitter_credentials_example.py](app/twitter_credentials_example.py) as twitter_credentials.py and fill in your true credentials.
    
    3. Run   
    ~~~~
    python setup.py install
    ~~~~
2. Go for it Tiger
  ~~~
  >>> from std import Dumper
  >>> dump = Dumper()
  >>> dump.loop_over_last_n_days(n=10)
  ~~~
3. Results will be saved to csv files (1 per day) in your the data folder

Few more options
---

Good to Know...
---

For now the default is to scrape only Hebrew tweets.
To scrape other languages:
~~~
# any
dump.lang = None

# only English
dump.lang = 'en'

# And so on...
~~~

TODO
---
- [ ] finish readme
