import numpy as np

from preprocess import Preprocessor
from metadata import Metadata
from tfrecords import TFRecordGenerator

pool_size = [10, 10, 3]
input_size = [2 * (2 * (2 * x + 1) + 1) + 1 for x in pool_size]
reference_size = [x + pad for x, pad in zip(input_size, [12, 12, 6])]
print('input_size', input_size)
print('record_size', reference_size)
k = 4
test_proportion = 0.25

data_path = '/vol/bitbucket/rh2515/MRI_Crohns'
label_path = '/vol/bitbucket/rh2515/MRI_Crohns/labels'
record_out_path = '/vol/bitbucket/rh2515/MRI_Crohns/tfrecords/ti_imb'
record_suffix = 'axial_t2_only'

abnormal_cases = list(range(70))
healthy_cases = list(range(100))
metadata = Metadata(data_path, label_path, abnormal_cases, healthy_cases, dataset_tag='')
# metadata = Metadata(data_path, label_path, abnormal_cases, healthy_cases, dataset_tag=' cropped')

print('Loading images...')
for patient in metadata.patients:
    print(f'Loading patient {patient.get_id()}')
    patient.load_image_data()

preprocessor = Preprocessor(constant_volume_size=reference_size)

metadata.patients = preprocessor.process(metadata.patients, ileum_crop=True, region_grow_crop=False, statistical_region_crop=False)

record_generator = TFRecordGenerator(record_out_path, record_suffix)
# record_generator.generate_train_test(test_proportion, metadata.patients)
record_generator.generate_cross_folds(k, metadata.patients)

print('Done')
