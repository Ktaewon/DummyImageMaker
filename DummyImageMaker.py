from PIL import Image
import requests
from io import BytesIO
from multiprocessing import Process


class DummyImageMaker():
    url = "https://picsum.photos/"
    
    def make(self, count, width, height, perProcessCount = 100):
        targetUrl = f"{self.url}/{width}/{height}"
        processCount = count // perProcessCount
        processes = []
        for processNum in range(processCount):
            start = processNum * perProcessCount
            end = (processNum + 1) * perProcessCount
            if end > count: end = count
            pr = Process(target = self.getAndSave,
                        args = (start, end, targetUrl, processNum))
            processes.append(pr)
        for process in processes:
            process.start()
        for process in processes:
            process.join()
    def getAndSave(self, start, end, targetUrl, processNum):
        for i in range(start, end):
            try:
                response = requests.get(targetUrl)
                img = Image.open(BytesIO(response.content))
                img.save(f"./dummy_images/dummy_{i}.jpg")
                print(f"#{processNum}: [dummy_{i}.jpg] saved")
            except Exception:
                print(Exception.with_traceback)


if __name__ == "__main__":
    dummpyImageMaker = DummyImageMaker()
    dummpyImageMaker.make(100000, 1920, 1080, 100)