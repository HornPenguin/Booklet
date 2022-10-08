from booklet.ui import HPMenu
from booklet.utils.misc import open_url 
from functools import partial


class HPBooklet_Menu(HPMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sub_entries.append(HelpMenu(self, self.main_app, self.ui_texts["help"], self.resources["help"], tearoff=0))
        self.sub_entries.append(ReferMenu(self, self.main_app, self.ui_texts["reference"], self.resources["reference"], tearoff=0))
        self.sub_entries.append(SettingMenu(self, self.main_app, self.ui_texts["settings"], self.resources["settings"], tearoff=0))
        self.sub_entries.append(LanguageMenu(self, self.main_app, self.ui_texts["language"], {}, tearoff=0))

        for label, menu in zip(self.ui_texts.values(), self.sub_entries):
            self.add_cascade(label=label["name"] , menu=menu)

class HelpMenu(HPMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_command(label= self.ui_texts["subentries"]["about"], command = self.__about_pop_up)
        self.add_command(label= self.ui_texts["subentries"]["license"], command = self.__license_pop_up)
        self.add_command(label= self.ui_texts["subentries"]["source"], command = self.__source_web_open)
    
    def __about_pop_up(self):
        self.main_app.pop_up(texts= self.resources["texts"]["about"])
    def __license_pop_up(self):
        self.main_app.pop_up(texts= self.resources["texts"]["license"], scroll_y=True)
    def __source_web_open(self):
        open_url(self.resources["urls"]["repository"])

class ReferMenu(HPMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_command(label = self.ui_texts["subentries"]["tutorial"], command= self.__tutorial_web_open)
        self.add_command(label = self.ui_texts["subentries"]["paper-format"], command= self.__paper_format_pop_up)
        self.add_command(label = self.ui_texts["subentries"]["paper-fold"], command= self.__paper_fold_pop_up)

    def __paper_format_pop_up(self):
        self.main_app.pop_up(self.resources["treeviews"]["paper_format"])
    def __paper_fold_pop_up(self):
        self.main_app.pop_up(self.resources["images"]["paper_fold"])
    def __tutorial_web_open(self):
        open_url(self.resources["urls"]["tutorial"])

class SettingMenu(HPMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_command(label = self.ui_texts["subentries"]["load"], command = self.__load)
        self.add_command(label = self.ui_texts["subentries"]["save"], command = self.__save)
    
    def __load(self):
        pass
    def __save(self):
        pass
    
class LanguageMenu(HPMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for lang in self.ui_texts["subentries"]:
            self.add_command(label = self.ui_texts["subentries"][lang], command= partial(self.__language_update, lang))
    
    def __language_update(self, code:str):
        self.main_app.update_ui_texts(code)
