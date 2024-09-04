import fiftyone as fo
from utils.config import dbParams

params = dbParams()
target_db = params.detail[0]

# Load your FiftyOne dataset
dataset = fo.Dataset.from_dir(
  dataset_type=params.types[target_db.type],
  dataset_dir=target_db.data_dir,
  images_path="train.txt",
  name=target_db.name,
  overwrite=True # this line should be removed
)
dataset.compute_metadata()

# Launch the app
session = fo.launch_app(dataset, remote=True, address="10.10.5.228", port=8080)
session.wait()