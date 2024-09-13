import argparse
import fiftyone as fo
import fiftyone.utils.random as four
from os import getcwd
import os.path as osp
from typing import Any

import sys
sys.path.insert(0, osp.dirname(osp.dirname(__file__)))
from formats import CvatImporter, Exporter
from formats.detail import dbDetail
from log import log

def load_argument() -> (Any | argparse.Namespace):
  parser = argparse.ArgumentParser(
    description="Split the raw data into train, val, and test subsets."
  )
  parser.add_argument(
    "--in_type", type=str, choices=["yolov4", "yolov5"], default="yolov4",
    help="The imported dataset format."
  )
  parser.add_argument(
    "--out_type", type=str, choices=["yolov4", "yolov5"], default="",
    help="The exported dataset format."
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
  # parser.add_argument(
  #   '-f', "--formula", type=str, default="random",
  #   choices=["random", "weighted", "balanced"],
  #   help="The split formula."
  # )

  args = parser.parse_args()
  if args.data_dir[-1] == '/':
    args.data_dir = args.data_dir[:-1]
  if args.name == "":
    args.name = osp.basename(args.data_dir)
  if args.out_type == "":
    args.out_type = args.in_type
  return args

if __name__ == "__main__":
  args = load_argument()
  test: bool = len(args.sizes) >= 3

  dataset = CvatImporter.load_yolov4(
    dbDetail.from_required(args.name, args.in_type, args.data_dir),
    args.images_list)

  try:
    subsets = CvatImporter.get_subsets(args.sizes)
  except ValueError as e:
    log.err(f"tools.spliter.py: {e}")

  # if args.formula == "random":
  #   four.random_split(dataset, subsets)
  # elif args.formula == "weighted":
  #   four.random_split(dataset, subsets)
  # elif args.formula == "balanced":
  #   four.random_split(dataset, subsets)

  # split the dataset
  views: list[fo.Dataset] = [dataset.match_tags("train"), dataset.match_tags("val")]
  if len(args.sizes) >= 3:
    views.append(dataset.match_tags("test"))

  # export the split subsets
  try:
    for split, view in zip(subsets, views):
      Exporter.dump(view, dbDetail.from_required(args.name, args.out_type), split)
  except Exception as e:
    log.err(f"tools.spliter.py: {e}")