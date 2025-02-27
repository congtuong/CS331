from pathlib import Path
from tqdm import tqdm
import shutil
import random

input_path = Path('/mlcv1/WorkingSpace/Personal/tuongbck/AIC2024/CoDETR/data/yolo_all_classes_sliced')

def load_data(split: str):
    root_dir = Path("/mlcv1/WorkingSpace/Personal/tuongbck/AIC2024/CoDETR/data/yolo_all_classes_sliced") / split
    print(root_dir/ "images")
    images = list((root_dir / "images").glob("*.jpg"))
    annotations = list((root_dir /  "labels").glob("*.txt"))
    

    return images, annotations

images_train, annotations_train = load_data("train")
images_val, annotations_val = load_data("val")
images_joined = images_train + images_val
annotations_joined = annotations_train + annotations_val

set_id = set([
    "_".join(t.stem.split("_")[:1])
    for t in images_joined
])

sorted(set_id)
print(len(images_joined), len(annotations_joined), len(set_id))
random.seed(42)
output_dir = Path("./sliced")
for _time in tqdm("ANME"):
    train_name = []
    val_name = []
    for _id in tqdm(set_id):
        # print(images_joined[0].stem.split("_"))
        images = [t for t in images_joined if f"{_id}_{_time}" in t.stem]
        annotations = [t for t in annotations_joined if f"{_id}_{_time}" in t.stem]
        print(len(images), len(annotations))
        joint = []
        for img in tqdm(images):
            for ann in annotations:
                if img.stem == ann.stem:
                    joint.append((img, ann))
        
        random.shuffle(joint)

        for i, (img, ann) in enumerate(joint):
            if img.stem != ann.stem:
                print(img, ann)
            if i < 0.8 * len(joint):
                train_name.append((img, ann))
            else:
                val_name.append((img, ann))
    (output_dir / _time / "train" / "images").mkdir(parents=True, exist_ok=True)
    (output_dir / _time / "val" / "images").mkdir(parents=True, exist_ok=True)
    (output_dir / _time / "train" / "labels").mkdir(parents=True, exist_ok=True)
    (output_dir / _time / "val" / "labels").mkdir(parents=True, exist_ok=True)
    print("Done making dir")
    print(len(train_name), len(val_name))
    print("Start copying...")
    for img, ann in tqdm(train_name):
        shutil.copy(img, output_dir / _time / "train" / "images")
        shutil.copy(ann, output_dir / _time / "train" / "labels")
    for img, ann in tqdm(val_name):
        shutil.copy(img, output_dir / _time / "val" / "images")
        shutil.copy(ann, output_dir / _time / "val" / "labels")

