#get access to libraries. This is ideal for video editing. 
from moviepy.editor import VideoFileClip 

#we need a class for video info. 
#Goal is to read file fps, duration, and size resolution 
class VideoInfo: 
    def __init__(self,file_path):
        self.file_path = file_path
        self.fps = None
        self.duration = None
        self.width = None
        self.height = None
#load video files and pushes data out
    def read_data(self): 
        with VideoFileClip(self.file_path) as clip: 
            #videofile is now converted to variable clip
            self.fps = clip.fps
            self.duration = clip.duration
            self.width, self.height = clip.size
        return {
            "fps": self.fps, 
            "duration": self.duration, 
            "width": self.width,
            "height": self.height
        }

class Video_Processor:
#creates changes to fps, duration, and size. MOdifications ftw
    def __init__(self):
        pass
    def apply_changes(self, new_fps = None, 
                      new_duration = None, new_width = None,
                      new_height = None, save_path = "output.mp4"):
        with VideoFileClip(self.file_path) as clip: 
            #fps change
            if new_fps: 
                clip = clip.set_fps(new_fps)

            #duration change. Condition that new duration is less than original.
            if new_duration and new_duration < clip.duration: 
                clip = clip.subclip(0, new_duration)
            #resoltution chnage
            if new_width and new_height:
                clip = clip.resize((new_width, new_height))

            #save the vid
            clip.write_videofile(save_path)

            return save_path

#testing 123 
if __name__ == "__main__": 
    print("test running rn")
    test_path = "Testing123.mp4"
    
    try: 
        #testing data reader
        info = VideoInfo(test_path)
        data = info.read_metadata()
        print("Video Info: ", data)

        #testing class Vid Processor
        processor = Video_Processor(test_path)
        processor.apply_changes(new_fps = 24, save_path = "week1_test_output.mp4")

    except Exception as errorMessage:
        print("Error: ", errorMessage)