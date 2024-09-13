import fiftyone as fo
import fiftyone.types
from typing import Callable
from .detail import dbDetail
from log import log

class CvatImporter:
  """
  Import cvat(labeltool) data into fiftyone Dataset
  """
  @staticmethod
  def get_subsets(sizes: list[float] = [0.8, 0.1, 0.1]) -> dict[str, float]:
    """
    Generate {name, portion} for each subsets, e.g. `{"train": 0.8}`

    Args:
      sizes: define each set size
    """
    if len(sizes) < 2:
      raise ValueError("There should at lease two subsets in a healthy dataset")

    subsets = {"train": sizes[0], "val": sizes[1]}
    if len(sizes) >= 3:
      subsets.update({"test": sizes[2]})
    return subsets

  @staticmethod
  def load_yolov4(detail: dbDetail, images_list: str = "train.txt") -> fo.Dataset:
    """
    Import CVAT YOLO 1.0 to an fiftyone.Dataset Object.

    Args:
      detail: database information
      images_list: the filename like `train.txt` specifying the location
      of the image listing file labels in `data_dir`.
    """
    return fo.Dataset.from_dir(
      dataset_type=fiftyone.types.YOLOv4Dataset,
      dataset_dir=detail.data_dir,
      images_path=images_list,
      name=detail.name,
      overwrite=True
    )

  @staticmethod
  def merge_dataset(datasets: list[fo.Dataset]) -> fo.Dataset:
    """
    Merge all dataset into one

    Args:
      datasets: it is recommended that these merged sets should come from same source
    """
    out_dataset: fo.Dataset = datasets.pop(0)

    for d in datasets:
      out_dataset.merge_samples(d)

class InternalImporter:
  """
  Internal functions for Importer, the one import fiftyone Dataset
  """
  @staticmethod
  def get_subsets(test: bool = True) -> list[str]:
    """
    Generate subsets name, i.e. `["train", "val", ("test")]`

    Args:
      test: include test set
    """
    subsets = ["train", "val"]
    if test:
      subsets = ["train", "val", "test"]
    return subsets

  @staticmethod
  def load_yolov4(dataset: fo.Dataset, detail: dbDetail, test: bool = True) -> None:
    """
    Import fiftyone.types.YOLOv4Dataset to an fiftyone.Dataset Object.

    Args:
      dataset: the Dataset Object
      detail: database information
      test: include test set
    """
    subsets = InternalImporter.get_subsets(test)

    dataset = fo.Dataset.from_dir(
      dataset_dir=f"{detail.data_dir}_{subsets[0]}",
      dataset_type=fiftyone.types.YOLOv4Dataset,
      tags=f"{subsets[0]}"
    )
    subsets.pop(0) # pop "train"

    for subset in subsets:
      # "val" and ("test")
      dataset.merge_dir(
        dataset_dir=f"{detail.data_dir}_{subset}",
        dataset_type=fiftyone.types.YOLOv4Dataset,
        tags=f"{subset}",
      )

  @staticmethod
  def load_yolov5(dataset: fo.Dataset, detail: dbDetail, test: bool = True) -> None:
    """
    Import fiftyone.types.YOLOv5Dataset to an fiftyone.Dataset Object.

    Args:
      dataset: the Dataset Object
      detail: database information
      test: include test set
    """
    subsets = InternalImporter.get_subsets(test)

    for subset in subsets:
      dataset.add_dir(
        dataset_dir=f"{detail.data_dir}",
        dataset_type=fiftyone.types.YOLOv5Dataset,
        split=subset,
        tags=subset
      )

class ImporterHashMap:
  FUNCS: dict[str, Callable[[fo.Dataset, dbDetail, bool], None]] = {
    "yolov4": InternalImporter.load_yolov4,
    "yolov5": InternalImporter.load_yolov5
  }

class Importer:
  """
  Import fiftyone Dataset
  """
  @staticmethod
  def load(dataset: fo.Dataset, detail: dbDetail, test: bool = True) -> bool:
    """
    Import a specified type to an fiftyone.Dataset Object.

    Args:
      dataset: the Dataset Object
      detail: database information
      test: include test set
    """
    try:
      # choose the function according to database type
      ImporterHashMap.FUNCS[detail.type](dataset, detail, test)
    except ValueError as e:
      log.err(f"{e}")
      return False
    return True