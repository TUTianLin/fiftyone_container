import fiftyone.types as dbTypes
import json
from typing import Dict, List

DBTYPES: Dict[str, dbTypes.Dataset] = {
  "yolo": dbTypes.YOLOv4Dataset
}

class dbDetail:
  name: str
  description: str
  type: dbTypes.Dataset
  data_dir: str
  img_counts: int

  def __init__(self, detail: dict) -> None:
    """Construct the database detail

    Args:
      detail: a detail for one dataset
      file (None): the path to the json file
        If None, the parameter will default to ``config/detail.json``
    """
    self.name = detail["name"]
    self.description = detail["description"]
    self.type = DBTYPES[detail["type"]]
    self.data_dir = detail["data_dir"]
    self.img_counts = detail["img_counts"]

  def __repr__(self) -> str:
    return f"dbDetail(name: {self.name}, description: {self.description}, type: {self.type}, data_dir: {self.data_dir}, img_counts: {self.img_counts})"""

class dbParams:
  detail: List[dbDetail] = []

  def __init__(self, detail_file=None) -> None:
    """Construct the params for the databases

    Args:
      detail_file (None): the path to the json file
        If None, the parameter will default to ``config/detail.json``
    """
    if detail_file == None:
      detail_file = "config/detail.json"

    with open(detail_file) as f:
      self.detail = [dbDetail(d) for d in json.load(f)["dataset"]]

  def __repr__(self) -> str:
    return f"detail: {self.detail}"