## Introduction
[Fiftyone](https://github.com/voxel51/fiftyone) is a data-cleaning open source that helps developers manage their datasets. I encapsulated the software in docker to make it easier to maintain, with only `pip install`.
The repository is still under development.

## Usage
build the docker image for fiftyone.
```bash
./scripts/build_service.sh
```

```bash
./scripts/service_up.sh # start the container
./scripts/service_down.sh # shutdown the container
```

run the test
```bash
root@my-pc:~/fiftyone# python main.py
```

## Reminder
Dataset format exported from CVAT may be inconsistent with fiftyone server, please compare two versions and make amendment by passing `XXX.txt` as image_list for `YOLO 1.0`(`yolov4`)[1].

[1]: I only corporate the yolov4 for different image_list text file name. If you encounter any other issue or wish for new feature, please make a new request in issues.
