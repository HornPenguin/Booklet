from booklet.ui import HPFrame, HPLabelFrame


class FileIO(HPFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


        self.sub_frames.append(
                Manuscript(
                    self, 
                    self.ui_texts["frames"]["manuscript"],
                    self.resources["files"]["manuscript"],
                    width = int(0.5*self.width),
                    height = int(0.75*self.height)
                )
            )
        self.sub_frames.append(
                FileInfo(
                    self, 
                    self.ui_texts["frames"]["file_info"],
                    self.resources["files"]["manuscript"],
                    width = int(0.5*self.width),
                    height = int(0.4*self.height)
                )
            )
        self.sub_frames.append(
                Output(
                    self, 
                    self.ui_texts["frames"]["output"],
                    self.resources["files"]["manuscript"],
                    width = int(0.5*self.width),
                    height = int(0.35*self.height)
                )
            )

        self.sub_frames[0].grid(row = 0, column = 0, rowspan = 2, padx = 10, pady = 2)
        self.sub_frames[1].grid(row = 0, column = 1, rowspan = 1, padx = 10, pady = 2)
        self.sub_frames[2].grid(row = 1, column = 1, rowspan = 1, padx = 10, pady = 2)
    
    @property
    def settings(self):
        pass
    @settings.setter
    def settings(self, *args):
        pass

class Manuscript(HPLabelFrame):
    # --------------------------
    # |      search_file       |
    # |------------------------| 
    # |             |          |
    # |    files    | buttons  |
    # |             |          |
    # --------------------------

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.grid_propagate(True)

        self.layout_frames = {
            "search_file": HPFrame(self, width=self.width),
            "files": HPFrame(self),
            "buttons": HPFrame(self, width= int(0.2*self.width)),
        }
class FileInfo(HPLabelFrame):
    # -----------------------
    # |             |       |
    # | left_labels | print |
    # |             |       |
    # -----------------------
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
class Output(HPLabelFrame):
    # --------------------------  
    # |             |          |
    # | left_labels |  inputs  |
    # |             |          |
    # |------------------------|
    # |       output_dir       |
    # --------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.layout_frames = {
            "left_label": HPFrame(self, width = int(0.33*self.width)),
            "name": HPFrame(self, width = int(0.33*self.width)),
            "output_dir": HPFrame(self, width = int(0.33*self.width)),
        }