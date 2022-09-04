from unittest import result
import src.posting.posting_repository as posting_repository
import datetime
from flask import jsonify # Return json form to client
import os # 파일 삭제

class PostingService:
    postingRepo = posting_repository.PostingRepository()

    def __init__(self) -> None:
        pass

    def saveImage(self, file, user_id):
        filePath = f'static/images/aramMenu/{user_id}{datetime.datetime.now()}.png'
        file.save(filePath)
        return filePath

    def deleteImage(self, path):
        os.remove(path)

    def insertPost(self, data):
        # edit data like [user_id, title, content, date, score, meal_time, image]
        try:
            res = self.postingRepo.insertPosting(data)
            return res
        except:
            return "Error: posting_service InsertData Error"

    def selectPost(self, post_id):
        try:
            result = self.postingRepo.selectPosting(post_id)
            print(result)
            return jsonify({"result":result})
        except:
            return "Error: posting_service SelectData Error"

    def updatePost(self, post_id, data):
        try:
            res = self.postingRepo.updatePosting(data)
            # 이미지 업데이트라면 기존 이미지 삭제
            return res
        except:
            return "Error: posting_service UpdateData Error"


    def deletePost(self, post_id):
        try:
            # 이미지 삭제
            path = self.postingRepo.getImagePath(post_id)
            if path == None:
                pass
            else:
                self.deleteImage(path)
            # 포스팅 데이터 삭제
            result = self.postingRepo.deletePosting(post_id)
            return jsonify({"result" : result})
        except:
            return "Error: posting_service DeletePostImg Error"

    def getPostList(self, times):
        try:
            result = self.postingRepo.getPostList(times)
            return jsonify({"result" : result})
        except:
            return "Error: posting_service DeletePost Error"
