googlenewsapi
+++++++++++++

API for searching Google News in Python

Features
++++++++

* Retrieval for each of the available topics
* Ad-hoc queries
* Creates Python objects out of JSON

Usage ::

from googlenews import GoogleNews
from googlenews import GoogleNewsResults
gnews = GoogleNews()
results = [GoogleNewsResults(r) for r in g.get_scitech()]

