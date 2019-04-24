import os
from enum import Enum

class SeriesTypes(Enum):
    AXIAL = 'Axial T2'
    CORONAL = 'Coronal T2'
    AXIAL_POSTCON = 'Axial Postcon'

class Patient:
    def __init__(self, group, index):
        self.group = group
        self.index = index

    def get_id(self):
        return self.group + str(self.index)

    def get_label(self):
        return int(self.group == 'A')

    def set_paths(self, axial, coronal, axial_postcon):
        self.axial = axial
        self.coronal = coronal
        self.axial_postcon = axial_postcon

    def set_images(self, axial_image=None):
        self.axial_image = axial_image

    def __str__(self):
        return f'{self.get_id()}: {self.axial}, {self.coronal}, {self.axial_postcon}'

class Metadata:
    def form_path(self, patient, series_type):
        path = os.path.join(self.data_path, patient.group, f'{patient.get_id()} {series_type}{self.data_extension}')
        if os.path.isfile(path):
            return path

    def file_list(self, patients):
        for patient in patients:
            axial = self.form_path(patient, SeriesTypes.AXIAL.value)
            coronal = self.form_path(patient, SeriesTypes.CORONAL.value)
            axial_postcon = self.form_path(patient, SeriesTypes.AXIAL_POSTCON.value)
            patient.set_paths(axial, coronal, axial_postcon)
        return patients

    def __init__(self, data_path):
        print('Forming metadata')
        self.data_path = data_path
        self.data_extension = '.nii'
        abnormal_cases = list(range(30))
        healthy_cases = list(range(30))

        abnormal_patients = [Patient('A', i + 1) for i in abnormal_cases]
        healthy_patients = [Patient('I', i + 1) for i in healthy_cases]

        self.patients = self.file_list(abnormal_patients + healthy_patients)