import json

class dbDetail:
  name: str
  description: str
  type: str
  data_dir: str
  img_counts: int

  def __init__(self, name: str, description: str, type: str, data_dir: str, img_counts: int) -> None:
    r"""Construct the database detail

    Args:
      name: dataset name
      description: detailed information about the db (database)
      type: db format
      data_dir: the path to the db
      img_counts: total img counts consist of `train`, `val`, and `test`
    """
    self.name = name
    self.description = description
    self.type = type
    self.data_dir = data_dir
    self.img_counts = img_counts

  @classmethod
  def from_dict(cls, detail: dict[str, str]):
    r"""Construct the database detail from dict()

    Args:
      detail: `dict` a detail for one dataset
    """
    return cls(detail["name"], detail["description"], detail["type"], detail["data_dir"], detail["img_counts"])

  def __repr__(self) -> str:
    return f"dbDetail(name: {self.name}, description: {self.description}, type: {self.type}, data_dir: {self.data_dir}, img_counts: {self.img_counts})"

  @classmethod
  def from_required(cls, name: str, type: str, data_dir: str = ""):
    r"""Construct the database detail with only the required parameters

    Args:
      name: dataset name
      type: db format
      data_dir: the path to the db
    """
    return cls(name, "", type, data_dir, 0)

def load_database_details(detail_file: str = None) -> list[dbDetail]:
  r"""Construct the params for the databases

  Args:
    detail_file (None): the path to the json file
      If None, the parameter will default to ``config/detail.json``
  """
  if detail_file == None:
    detail_file = "config/detail.json"

  details: list[dbDetail] = []
  with open(detail_file) as f:
    details = [dbDetail.from_dict(d) for d in json.load(f)["dataset"]]
  return details