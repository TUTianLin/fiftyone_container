import fiftyone as fo
from formats import load_database_details, Importer

params = load_database_details()
target_db = params[0]

dataset = fo.Dataset(name=target_db.name, overwrite=True)
Importer.load(dataset, target_db, False)
dataset.compute_metadata()

# Launch the app
session = fo.launch_app(dataset, remote=True, address="10.10.5.228", port=8080)
session.wait()