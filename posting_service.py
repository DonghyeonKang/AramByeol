import posting_repository
import datetime

class postingService:
    postingRepo = posting_repository.postingRepository()

    def __init__(self) -> None:
        pass

    def saveImage(self, file, user_id):
        filePath = f'static/images/aramMenu/{user_id}{datetime.datetime.now()}.png'
        file.save(filePath)
        return filePath

    def insertData(self, data):
        # edit data like [user_id, title, content, date, category, score, meal_time, image]
        try:
            res = self.postingRepo.insertPosting(data)
            return res
        except:
            return "Error: posting_service InsertData Error"