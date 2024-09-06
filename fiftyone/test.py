import fiftyone as fo
from utils.config import dbParams, DBTYPES

params = dbParams()
target_db = params.detail[0]

dataset = fo.Dataset.from_dir(
  dataset_type=target_db.type,
  dataset_dir=f"{target_db.data_dir}_train",
  name=target_db.name,
  tags="train",
  overwrite=True # this line should be removed
)
dataset.merge_dir(
  dataset_type=target_db.type,
  dataset_dir=f"{target_db.data_dir}_val",
  tags="validation",
)
dataset.compute_metadata()

# Launch the app
session = fo.launch_app(dataset, remote=True, address="10.10.5.228", port=8080)
session.wait()