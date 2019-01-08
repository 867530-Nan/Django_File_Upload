from django.db import models, connection

from sklearn.feature_extraction.text import CountVectorizer

class Upload(models.Model):
    title = models.CharField(max_length=100)
    upload = models.FileField(upload_to="media/")

    def __str__(self):
        return self.title

<<<<<<< HEAD
class Word(models.Model):
    token = models.TextField(unique=True)
    count = models.IntegerField()
    frequency = models.FloatField(null=True)

    def count_vectorizer(text):
        vectorizer = CountVectorizer(token_pattern=r"\b[\w']+\b", analyzer="word")
        tokens = vectorizer.fit([text]).get_feature_names() 
        freq = vectorizer.transform([text]).toarray()[0].tolist() 
        data = [list(t) for t in zip(tokens, freq)]
        with connection.cursor() as cursor: 
            cursor.executemany(  
                "INSERT INTO uploads_word(token,count)\
                VALUES (%s,%s) ON CONFLICT (token)\
                DO UPDATE SET count = excluded.count + uploads_word.count;", data)
            cursor.execute(
                "WITH new_values AS (SELECT id, count / (SELECT SUM(count)::FLOAT FROM uploads_word) AS freq FROM uploads_word)\
                update uploads_word as old_values\
                set frequency = new_values.freq\
                from new_values new_values\
                where new_values.id = old_values.id;"          
            )      

    def _str_(self):
        return self.token
=======

class URLUpload(models.Model):
    title = models.TextField()
    url_upload = models.TextField()

    def __str__(self):
        return self.title
>>>>>>> fetching
