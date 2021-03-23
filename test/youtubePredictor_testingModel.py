# @TODO import database object as db

import DiTTo_YoutubePredictor.youtubePredictor_constants as ypConst


class VideoStats(db.Model):
    __tablename__ = ypConst.DATABASE_NAME

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    anger = db.Column(db.Boolean, nullable=False)
    disgust = db.Column(db.Boolean, nullable=False)
    fear = db.Column(db.Boolean, nullable=False)
    joy = db.Column(db.Boolean, nullable=False)
    sadness = db.Column(db.Boolean, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __init__(self, url, anger, disgust, fear, joy, sadness, views):
        self.url = url
        self.anger = anger
        self.disgust = disgust
        self.fear = fear
        self.joy = joy
        self.sadness = sadness
        self.views = views

    def __repr__(self):
        return '<url {}>'.format(self.url)

    def get_id(self):
        return self.id

    def get_views(self):
        return self.views

    def get_tones(self):
        return {'anger:': self.anger,
                'disgust:': self.disgust,
                'fear:': self.fear,
                'joy:': self.joy,
                'sadness:': self.sadness
                }
