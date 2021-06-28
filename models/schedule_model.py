
class Schedule(db.Model):
    token = db.Column(db.Integer(), primary_key=True)
    weekday = db.Column(db.String(), nullable=False)
    voucher_num = db.Column(db.Integer(), nullable=False)
    discount = db.Column(db.Integer(), nullable=False)
    start = db.Column(db.String(), nullable=False)
    end = db.Column(db.String(), nullable=False)
    eatery_id = db.Column(db.Integer(), nullable=False, unique=True)
    def __repr__(self):
        return f'Schedule {self.eatery_id}'