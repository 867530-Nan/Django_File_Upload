from django.db import models, connection

from sklearn.feature_extraction.text import CountVectorizer


class Upload(models.Model):
    title = models.CharField(max_length=100)
    upload = models.FileField(upload_to="media/")

    def __str__(self):
        return self.title


class URLUpload(models.Model):
    title = models.TextField()
    url_upload = models.TextField()

    def __str__(self):
        return self.title


class Word(models.Model):
    token = models.TextField(unique=True)
    count = models.IntegerField()
    frequency = models.FloatField(null=True)

    def count_vectorizer(text):
        vectorizer = CountVectorizer(
            token_pattern=r"\b[\w']+\b", analyzer="word")
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
<<<<<<< 663b9c63628569a5964e2c416e36a64c8096fd0c
=======

class NGram(models.Model):
    token = models.TextField()
    n_gram = models.TextField()
    count = models.IntegerField()
    frequency = models.FloatField(null=True)
    class Meta:
        unique_together = ('token', 'n_gram')

    def count_vectorizer(text):
        vectorizer = CountVectorizer(token_pattern=r"\b[\w']+\b", analyzer="word", ngram_range=(3,3), min_df=1)
        tokens = vectorizer.fit([text]).get_feature_names() 
        freq = vectorizer.transform([text]).toarray()[0].tolist() 
        n_grams = []
        for i, t in enumerate(tokens):
            words = t.split()
            n_grams.append([words[0] + ' ' + words[1], words[2], freq[i]])
        with connection.cursor() as cursor: 
            cursor.executemany(  
                "INSERT INTO uploads_ngram(token,n_gram,count)\
                VALUES (%s,%s, %s) ON CONFLICT (token, n_gram)\
                DO UPDATE SET count = excluded.count + uploads_ngram.count", 
                n_grams)
            cursor.execute(
                "WITH new_values AS (SELECT id, count / (SELECT SUM(count)::FLOAT FROM uploads_word) AS freq FROM uploads_ngram)\
                update uploads_ngram as old_values\
                set frequency = new_values.freq\
                from new_values new_values\
                where new_values.id = old_values.id;"          
            )    

    def _str_(self):
        return self.token
>>>>>>> ngram processing
