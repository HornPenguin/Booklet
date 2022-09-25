

class SectionCompositon:
    #Validation
    @staticmethod
    def validate_fold_sequence():
        pass
    @staticmethod
    def validate_crease_pattern():
        pass
    @staticmethod
    def validate_face_matrix():
        pass
    #Fold determinator conversion routines 
    @staticmethod
    def convert_fs2cp():
        pass
    @staticmethod
    def convert_fs2m():
        pass
    @staticmethod
    def convert_cp2fs():
        pass
    @staticmethod
    def convert_cp2m():
        pass
    @staticmethod
    def convert_m2fs():
        pass
    @staticmethod
    def convert_m2cp():
        pass

    def __init__(self, fold_sequence):
        if not self.validate_fold_sequence(fold_sequence):
            raise ValueError("Invaild fold sequence.")
        self.fold_sequence = fold_sequence
        self.creases_pattern = self.convert_fs2cp(self.fold_sequence)
        self.face_matrix = self.convert_fs2m(self.fold_sequence)
        pass

    @classmethod
    def from_creases_pattern(cls):
        pass
    @classmethod
    def from_matrix(cls, list2dim):
        row, column = len(list2dim), len(list2dim[0])
        pass
    @classmethod
    def leaves_expln2_n(cls, leaves:int, insert:int):
        pass

