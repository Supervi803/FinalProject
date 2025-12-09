#get access to libraries. This is ideal for video editing. 
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip 
import moviepy

#stores video path and initializes attributes as "None"
#__init__ is called when creating a new VideoInfo object
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
            #dictionary
        return {
            "fps": self.fps, 
            "duration": self.duration, 
            "width": self.width,
            "height": self.height
        }

class Video_Processor:
#creates changes to fps, duration, and size. MOdifications ftw
#holds the path of video if wanting to modify it
    def __init__(self, file_path):
        self.file_path = file_path
        
    def apply_changes(self, new_fps = None, 
                      new_duration = None, new_width = None,
                      new_height = None, save_path = "output.mp4"):
        try: 
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
        except Exception as errorMessage:
            raise errorMessage

#GUI class for buttons
#main tkinter window
class VideoEditorGUI: 
    def __init__(self, master):
        self.master = master
        #window title
        master.title("video editor")
        #store selected video path and stores VideoInfo object
        self.video_path = None
        self.video_info = None

        #the buttons that is for inputs

        #open file dialog
        self.select_button = tk.Button(master, text="Select Video", command=self.select_video)
        self.select_button.grid(row=0, column=0, padx=5, pady=5)
        #padx and pady adds space around button

        #read data from selected videos and fill the entry fields
        self.load_button = tk.Button(master, text="Load Info", command=self.load_video_info)
        self.load_button.grid(row=0, column=1, padx=5, pady=5)

        #use Video_Processor to apply changes and save into new video file

        self.save_button = tk.Button(master, text="Apply Changes", command=self.apply_changes)
        
        #arrange the buttons in a row w/ spacing
        self.save_button.grid(row=0, column=2, padx=5, pady=5)

        #lables for info display
        tk.Label(master, text="FPS:").grid(row=1, column=0)
        tk.Label(master, text="Duration (sec):").grid(row=2, column=0)
        tk.Label(master, text="Width:").grid(row=3, column=0)
        tk.Label(master, text="Height:").grid(row=4, column=0)

        #allow user input to change properties
        self.fps_entry = tk.Entry(master)
        self.fps_entry.grid(row=1, column=1)
        self.duration_entry = tk.Entry(master)
        self.duration_entry.grid(row=2, column=1)
        self.width_entry = tk.Entry(master)
        self.width_entry.grid(row=3, column=1)
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=4, column=1)

# button functions
    def select_video(self):
            self.video_path = filedialog.askopenfilename(
                filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
            if self.video_path:
                messagebox.showinfo("Video Selected", f"Selected: {self.video_path}")

    def load_video_info(self):
        if not self.video_path:
            messagebox.showerror("Error", "You gotta select a video first!")
            return
        # checks if video is selected, if not, then a error popup appears
        #fills input boxes with values
        try:
            self.video_info = VideoInfo(self.video_path)
            data = self.video_info.read_data()
            self.fps_entry.delete(0, tk.END)
            self.fps_entry.insert(0, data["fps"])
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, round(data["duration"], 2))
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, data["width"])
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, data["height"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load video info:\n{e}")
    #read values from input which converts to numbers
    #if an input is empty, result is NOne
    #calls Video_Processor.apply_changes to create a new video
    def apply_changes(self):
            if not self.video_path:
                messagebox.showerror("Error", "You gotta select a video first!")
                return
            try:
                new_fps = float(self.fps_entry.get()) if self.fps_entry.get() else None
                new_duration = float(self.duration_entry.get()) if self.duration_entry.get() else None
                new_width = int(self.width_entry.get()) if self.width_entry.get() else None
                new_height = int(self.height_entry.get()) if self.height_entry.get() else None

                processor = Video_Processor(self.video_path)
                processor.apply_changes(
                    new_fps=new_fps,
                    new_duration=new_duration,
                    new_width=new_width,
                    new_height=new_height,
                    save_path="output.mp4"
                )
                messagebox.showinfo("Awesome! It's successful!", "Video saved as output.mp4")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process video:\n{e}")

# root = tk.TK() creates a main window
# VideoEditorGUI(root) initialize GUI layout
# root.mainloop() start event loop, window stay open + responsive
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoEditorGUI(root)
    root.mainloop()