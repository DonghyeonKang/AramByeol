import src.posting.posting_repository as posting_repository
import datetime

class PostingService:
    postingRepo = posting_repository.PostingRepository()

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

    def selectData(self, post_id):
        try:
            res = self.postingRepo.selectPosting()
            return res
        except:
            return "Error: posting_service SelectData Error"

    def updateData(self, post_id, data):
        try:
            res = self.postingRepo.updatePosting(data)
            return res
        except:
            return "Error: posting_service UpdateData Error"


    def deleteData(self, post_id):
        try:
            res = self.postingRepo.deletePosting()
            return res
        except:
            return "Error: posting_service DeleteData Error"

