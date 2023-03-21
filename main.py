try: 
    import boto3
    import pandas as pd
    import csv
    import time
    from itertools import cycle
    from shutil import get_terminal_size
    from threading import Thread


    print("Hurry!! All modules are loaded successfully...")

except Exception as e:
    print("Please look into it few moduls are missing here {}",format(e))

class Loader:

    def __init__(self, description="Loading...", end_point="Done!", time_out=0.2):

        self.desc = description
        self.end = end_point
        self.timeout = time_out

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for i in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {i}", flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()


class csvReader(object):


    def __init__(self, S3_Bucket=''):
        self.S3_Bucket= S3_Bucket
        self.client = boto3.client('s3')
        self.response = self.client.list_objects(Bucket=self.S3_Bucket)
        
       
    def get_data(self):

        return [x.get("Key", None) for x in self.response.get("Contents", None)]
        


    def get_data_frame(self, Key=''):
        data = self.client.get_object(Bucket=self.S3_Bucket, Key=Key)
        data_frame = data["Body"].read().decode("utf-8")
        data_frame=csv.reader(data_frame.split('\r\n'))
        data=[]
        main=next(data_frame)
        for row in data_frame:
            data.append(row)
        frame= pd.DataFrame(data=data,columns=main)
        return frame
        
if __name__ == "__main__":
    with Loader("Loading for CSV..."):
        for i in range(3):
            time.sleep(0.25)

    loader = Loader("Loading for CSV details...", "oohhh!!, That was too fast!", 0.05).start()
    for i in range(3):
        time.sleep(0.25)

    loader.stop()

if __name__=="__main__":
    obj = csvReader(S3_Bucket="test-s3-velero")
    print("This is you CSV data")
    # print(obj.get_data)
    print(obj.get_data_frame(Key="states_by_country_code.csv").head())

        