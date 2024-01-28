from django.db import models
import os, subprocess, time, threading
# Create your models here.

class Show(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200)
    show = models.ForeignKey(Show, on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey("Season", on_delete=models.SET_NULL, null=True)
    epNum = models.IntegerField()
    file = models.FileField(default=None, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        
        # Call the original save method to save the instance
        super().save(*args, **kwargs)
        
        # Call the getHlsNecessities method after saving
        self.detachThread()
    
    def getHlsNecessities(self):
        if self.file and self.id is not None:
            # Use the id of the Episode instance, not the FileField object
            fID = self.id
            file_path = os.path.dirname(os.path.abspath(self.file.path)) + f"\{self.file.name}"

            # Create folder with ID as name (in static)
            folder_path = os.path.join('static', str(fID)) #makes problems
            os.makedirs(folder_path, exist_ok=True)

            ts = os.path.join(folder_path, 'segment_%05d.ts')
            m3u8 = os.path.join(folder_path, 'playlist.m3u8')

            # FFmpeg command to create HLS playlist and segments

            command = f"ffmpeg -i \"{file_path}\" -c:a aac -b:a 128k -c:v libx264 -crf 18 -flags -global_header -map 0 -f segment -segment_time 10 -segment_list \"{m3u8}\" -segment_format mpegts -c:s:0 copy \"{ts}\""
            subprocess.call(command, shell=True)

            print("------HLS IS NOW COMPLETE------")
            os.remove(file_path)
    
    def detachThread(self):
        global ffmpeg_thread
        ffmpeg_thread = threading.Thread(target=self.getHlsNecessities)
        ffmpeg_thread.start()


    def __str__(self):
        return f"{self.epNum}"

class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=models.SET_NULL, null=True)
    seasonNum = models.IntegerField(default=1, null=True)

    def __str__(self):
        return f"{self.seasonNum} | {self.show}"