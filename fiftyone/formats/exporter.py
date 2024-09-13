import fiftyone as fo
import fiftyone.types
import os.path as osp
import shutil
from typing import Callable
from .detail import dbDetail
from log import log

class InternalExporter:
  """
  Internal functions for Exporter, the one export fiftyone Dataset
  """
  @staticmethod
  def get_target_path(name: str, dataset_dir: str = "db") -> str:
    """
    Get target path to export the following dataset

    Args:
      name: the database name
      dataset_dir: the directory of all the datasets
    """
    return f"{dataset_dir}/{name}"

  @staticmethod
  def dump_yolov4(dataset: fo.Dataset, target_path: str, split: str = "train") -> None:
    """
    Export an fiftyone.Dataset Object in Yolov4.

    Args:
      dataset: the Dataset Object
      target_path: the location of the exported dataset
      split: the subset group, e.g. `train`
    """
    target_path = f"{target_path}_{split}"
    if osp.exists(target_path):
      shutil.rmtree(target_path)

    dataset.export(
      export_dir=target_path,
      dataset_type=fiftyone.types.YOLOv4Dataset
    )

  @staticmethod
  def dump_yolov5(dataset: fo.Dataset, target_path: str, split: str = "train") -> None:
    """
    Export an fiftyone.Dataset Object in Yolov5.

    Args:
      dataset: the Dataset Object
      target_path: the location of the exported dataset
      split: the subset group, e.g. `train`
    """
    if osp.exists(target_path) and split == "train":
      shutil.rmtree(target_path)
    dataset.export(
      export_dir=target_path,
      dataset_type=fiftyone.types.YOLOv5Dataset,
      split=split
    )

class ExporterHashMap:
  FUNCS: dict[str, Callable[[fo.Dataset, str, str], None]] = {
    "yolov4": InternalExporter.dump_yolov4,
    "yolov5": InternalExporter.dump_yolov5
  }

class Exporter:
  """
  Export fiftyone Dataset
  """

  @staticmethod
  def dump(dataset: fo.Dataset, detail: dbDetail, split: str = "train") -> bool:
    """
    Export an fiftyone.Dataset Object in a specified format.

    Args:
      dataset: the Dataset Object
      detail: database information
      split: the subset group, e.g. `train`
    """
    try:
      target_path = InternalExporter.get_target_path(detail.name)
      ExporterHashMap.FUNCS[detail.type](dataset, target_path, split)
    except Exception as e:
      log.err(f"{e}")
      return False
    return True