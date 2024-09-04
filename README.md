## Introduction
[Fiftyone](https://github.com/voxel51/fiftyone) is a data-cleaning open source that helps developers manage their datasets. I encapsulated the software in docker to make it easier to maintain, with only `pip install`.
The repository is still under development.

## Usage
build the docker image for fiftyone.
```bash
cd fiftyone
./scripts/build_service.sh
```

```bash
./scripts/service_up.sh # start the container
./scripts/service_down.sh # shutdown the container
```

run the test
```bash
root@my-pc:~/fiftyone# python test.py
```

## Reminder
yolo format needed to be like this. You may have to tweak file name in test.py if your txt file is not `train.txt`.
```bash
- my-yolo-dataset
    |--- data/     # imgs
    |--- obj.names # classes
    |--- train.txt # the list of imgs' locations
```
