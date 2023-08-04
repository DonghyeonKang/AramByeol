import src.repository.ViewRepository  as ViewRepository

class ViewService:
    # viewRepository 객체 생성
    viewRepository = ViewRepository.ViewRepository()

    def getView(self):
        result = ViewRepository.selectView()
        return result