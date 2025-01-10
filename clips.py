import datetime


class Clip:
  
    def __init__(self, title, embed_url, thumbnail_url, created_at):
        self.title = title
        self.embed_url = embed_url + "&parent=127.0.0.1"
        self.thumbnail_url = thumbnail_url
        self.created_at = self.convertTime(created_at)
        self.unix_created_at = self.rfc3339_to_unix(created_at)

    def convertTime(self, created_at : str):
        date = created_at.split("T")[0]
        time = created_at.split("T")[1]
        time = time.split("Z")[0]

        date = date.split("-")
        return date[2] + "." + date[1] + "." + date[0] + " " + time
    
    def __str__(self):
        return f"{self.title} {self.embed_url}"

    def rfc3339_to_unix(self, time):
        dt = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        unix_time = dt.timestamp()
        return int(unix_time)


  