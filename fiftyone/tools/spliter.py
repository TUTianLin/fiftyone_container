import argparse
import fiftyone as fo
import fiftyone.utils.random as four
import os.path as osp
import sys
from typing import Any

sys.path.append(osp.abspath("/root/fiftyone"))
from utils.config import DBTYPES

def load_argument() -> (Any | argparse.Namespace):
  parser = argparse.ArgumentParser(
    description="Split the raw data into train, val, and test subsets."
  )
  parser.add_argument(
    '-t', "--type", type=str, choices=["yolo"], default="yolo",
    help="The imported dataset format."
  )
  parser.add_argument(
    '-d', "--data_dir", type=str, required=True,
    help="The parent directory of the raw dataset."
  )
  parser.add_argument(
    "--images_list", type=str, default="train.txt",
    help="Yolo dataset store the images location in one txt file, i.e. `train.txt`."
  )
  parser.add_argument(
    '-n', "--name", type=str, default="", help="The project name."
  )
  parser.add_argument(
    '-s', "--sizes", type=float, nargs='+',
    default=[0.8, 0.1, 0.1],
    help="The subset sizes of train, val, and test. You can omit the test size, default: 0.8 0.1 0.1"
  )

  args = parser.parse_args()
  if args.data_dir[-1] == '/':
    args.data_dir = args.data_dir[:-1]
  if args.name == "":
    args.name = osp.basename(args.data_dir)

  return args

if __name__ == "__main__":
  args = load_argument()

  dataset = fo.Dataset.from_dir(
    dataset_type=DBTYPES[args.type],
    dataset_dir=args.data_dir,
    images_path=args.images_list,
    name=args.name,
    overwrite=True
  )

  # declare the sizes of each subsets
  subsets = {"train": args.sizes[0], "val": args.sizes[1]}
  if len(args.sizes) >= 3:
    subsets.update({"test": args.sizes[2]})
  four.random_split(dataset, subsets)

  # split the dataset
  train_view: fo.Dataset = dataset.match_tags("train")
  val_view: fo.Dataset = dataset.match_tags("val")
  test_view: fo.Dataset = None
  if len(args.sizes) >= 3:
    test_view = dataset.match_tags("test")

  # export the split subsets
  target_path = f"db/{args.name}"
  train_view.export(
    export_dir=f"{target_path}_train",
    dataset_type=DBTYPES[args.type]
  )
  val_view.export(
    export_dir=f"{target_path}_val",
    dataset_type=DBTYPES[args.type]
  )
  if len(args.sizes) >= 3:
    test_view.export(
      export_dir=f"{target_path}_test",
      dataset_type=DBTYPES[args.type]
    )