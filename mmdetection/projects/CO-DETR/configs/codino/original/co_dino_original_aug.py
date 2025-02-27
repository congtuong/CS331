_base_ = ["co_dino_5scale_r50_8xb2_1x_coco.py"]

pretrained = "https://github.com/SwinTransformer/storage/releases/download/v1.0.0/swin_large_patch4_window12_384_22k.pth"  # noqa
load_from = "https://download.openmmlab.com/mmdetection/v3.0/codetr/co_dino_5scale_swin_large_16e_o365tococo-614254c9.pth"  # noqa
# load_from = './mmdetection/work_dirs/co_dino_5scale_swin_l_16xb1_16e_o365tococo/last_checkpoint'

data_root = "/mlcv1/WorkingSpace/Personal/tuongbck/AIC2024/CoDETR/data/splited"
backend_args = None
dataset_type = "CocoDataset"
classes = ("bus", "bicycle", "car", "person", "truck")
num_classes = len(classes)

# model settings
model = dict(
    backbone=dict(
        _delete_=True,
        type="SwinTransformer",
        pretrain_img_size=384,
        embed_dims=192,
        depths=[2, 2, 18, 2],
        num_heads=[6, 12, 24, 48],
        window_size=12,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.0,
        attn_drop_rate=0.0,
        drop_path_rate=0.3,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        # Please only add indices that would be used
        # in FPN, otherwise some parameter will not be used
        with_cp=True,
        convert_weights=True,
        init_cfg=dict(type="Pretrained", checkpoint=pretrained),
    ),
    neck=dict(in_channels=[192, 384, 768, 1536]),
    query_head=dict(
        dn_cfg=dict(box_noise_scale=0.4, group_cfg=dict(num_dn_queries=500)),
        transformer=dict(encoder=dict(with_cp=6)),
    ),
)

# load_pipeline = [
#     dict(type="LoadImageFromFile"),
#     dict(type="LoadAnnotations", with_bbox=True),
#     dict(
#         type="RandomChoice",
#         transforms=[
#             [
#                 dict(
#                     type="RandomChoiceResize",
#                     scales=[
#                         (480, 2048),
#                         (512, 2048),
#                         (544, 2048),
#                         (576, 2048),
#                         (608, 2048),
#                         (640, 2048),
#                         (672, 2048),
#                         (704, 2048),
#                         (736, 2048),
#                         (768, 2048),
#                         (800, 2048),
#                         (832, 2048),
#                         (864, 2048),
#                         (896, 2048),
#                         (928, 2048),
#                         (960, 2048),
#                         (992, 2048),
#                         (1024, 2048),
#                         (1056, 2048),
#                         (1088, 2048),
#                         (1120, 2048),
#                         (1152, 2048),
#                         (1184, 2048),
#                         (1216, 2048),
#                         (1248, 2048),
#                         (1280, 2048),
#                         (1312, 2048),
#                         (1344, 2048),
#                     ],
#                     keep_ratio=True,
#                 )
#             ],
#             [
#                 dict(
#                     type="RandomChoiceResize",
#                     scales=[(400, 4200), (500, 4200), (600, 4200)],
#                     keep_ratio=True,
#                 ),
#                 dict(
#                     type="RandomCrop",
#                     crop_type="absolute_range",
#                     crop_size=(384, 600),
#                     allow_negative_crop=True,
#                 ),
#                 dict(
#                     type="RandomChoiceResize",
#                     scales=[
#                         (480, 2048),
#                         (512, 2048),
#                         (544, 2048),
#                         (576, 2048),
#                         (608, 2048),
#                         (640, 2048),
#                         (672, 2048),
#                         (704, 2048),
#                         (736, 2048),
#                         (768, 2048),
#                         (800, 2048),
#                         (832, 2048),
#                         (864, 2048),
#                         (896, 2048),
#                         (928, 2048),
#                         (960, 2048),
#                         (992, 2048),
#                         (1024, 2048),
#                         (1056, 2048),
#                         (1088, 2048),
#                         (1120, 2048),
#                         (1152, 2048),
#                         (1184, 2048),
#                         (1216, 2048),
#                         (1248, 2048),
#                         (1280, 2048),
#                         (1312, 2048),
#                         (1344, 2048),
#                     ],
#                     keep_ratio=True,
#                 ),
#             ],
#         ],
#     ),
#     dict(type="RandomFlip", prob=0.5),
#     dict(type="RandomAffine"),
#     dict(type="Brightness", prob=0.5),
#     # dict(type='Pad', size=img_size),
#     # dict(type="Collect", keys=["img", "gt_bboxes", "gt_labels"]),
# ]

image_size = (1536, 1536)
load_pipeline = [
    dict(type="LoadImageFromFile"),
    dict(type="LoadAnnotations", with_bbox=True),
    dict(
        type="Resize",
        scale=image_size,
        scale_factor=(0.5, 1.5),
        keep_ratio=True,
    ),
    dict(
        type="RandomCrop",
        crop_type="absolute_range",
        crop_size=image_size,
        allow_negative_crop=True,
    ),
    dict(type="FilterAnnotations", min_gt_bbox_wh=(1e-2, 1e-2)),
    dict(type="RandomFlip", prob=0.5),
    dict(type="Pad", size=image_size, pad_val=dict(img=(114, 114, 114))),
]
# train_pipeline = [
#     dict(type='CopyPaste', max_num_pasted=100),
#     dict(type='DefaultFormatBundle'),
#     dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks']),
# ]

train_pipeline = [
    dict(type="CopyPaste", max_num_pasted=100, paste_by_box=True),
    dict(type="PackDetInputs"),
]

# train_dataloader = dict(
#     batch_size=1, num_workers=1, dataset=dict(pipeline=train_pipeline))

train_dataloader = dict(
    batch_size=1,
    num_workers=4,
    dataset=dict(
        type="MultiImageMixDataset",
        dataset=dict(
            type=dataset_type,
            data_root=data_root,
            ann_file="train.json",
            data_prefix=dict(img="train/images"),
            backend_args=backend_args,
            pipeline=load_pipeline,
        ),
        pipeline=train_pipeline,
    ),
)

test_pipeline = [
    dict(type="LoadImageFromFile"),
    dict(type="Resize", scale=(2048, 1280), keep_ratio=True),
    dict(type="LoadAnnotations", with_bbox=True),
    dict(
        type="PackDetInputs",
        meta_keys=("img_id", "img_path", "ori_shape", "img_shape", "scale_factor"),
    ),
]

train_dataset = dict(type="MultiImageMixDataset")

# val_dataloader = dict(dataset=dict(pipeline=test_pipeline))
val_dataloader = dict(
    batch_size=1,
    dataset=dict(
        type=dataset_type,
        pipeline=test_pipeline,
        # classes=classes,
        data_root=data_root,
        ann_file="val.json",
        data_prefix=dict(img="val/images"),
        backend_args=backend_args,
    ),
)

test_dataloader = val_dataloader

val_evaluator = dict(  # Validation evaluator config
    type="CocoMetric",  # The coco metric used to evaluate AR, AP, and mAP for detection and instance segmentation
    # classes=classes,  # Classes to be evaluated
    ann_file=data_root + "/val.json",  # Annotation file path
    metric=[
        "bbox"
    ],  # Metrics to be evaluated, `bbox` for detection and `segm` for instance segmentation
    format_only=False,
    backend_args=backend_args,
)

test_evaluator = val_evaluator

optim_wrapper = dict(optimizer=dict(lr=1e-4))

max_epochs = 20
train_cfg = dict(max_epochs=max_epochs)

param_scheduler = [
    dict(
        type="MultiStepLR",
        begin=0,
        end=max_epochs,
        by_epoch=True,
        milestones=[8],
        gamma=0.1,
    )
]
