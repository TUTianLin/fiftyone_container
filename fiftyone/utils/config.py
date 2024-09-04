import fiftyone.types as dbTypes
import json
from typing import Any, Dict, List
import yaml

class dbDetail:
  name: str
  description: str
  type: str
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
    self.type = detail["type"]
    self.data_dir = detail["data_dir"]
    self.img_counts = detail["img_counts"]

  def __repr__(self) -> str:
    return f"dbDetail(name: {self.name}, description: {self.description}, type: {self.type}, data_dir: {self.data_dir}, img_counts: {self.img_counts})"""

class dbParams:
  detail: List[dbDetail] = []
  types: Dict[str, Any] = {}

  def __init__(self, detail_file=None, type_file=None) -> None:
    """Construct the params for the databases

    Args:
      detail_file (None): the path to the json file
        If None, the parameter will default to ``config/detail.json``
    """
    if detail_file == None:
      detail_file = "config/detail.json"

    with open(detail_file) as f:
      self.detail = [dbDetail(d) for d in json.load(f)["dataset"]]
    self.load_types()

  def __repr__(self) -> str:
    return f"detail: {self.detail}, types: {self.types}"

  def load_types(self):
    self.types = {
      "yolo": dbTypes.YOLOv4Dataset
    }