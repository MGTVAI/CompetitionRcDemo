# 首届 "马栏山"杯国际音视频算法大赛 推荐赛道demo说明

# demo 使用说明

```
pip install -r requirements.txt
export DATA_DIR=<the data dir>
bash  run.sh train_eval
```

use docker to run
```
make run
```

# docker 镜像说明

进入获奖名单中的用户需要提交可训练、可复现的docker image

## docker 格式说明

* 选手可以选`amd64`下、OS为`linux`的任意基础镜像环境
* 验证机器使用普通非GPU 机器8核32G 机器，选手的训练脚本应能在`12hour`内完成训练
* 数据将挂载在/data/ 目录下，docker image中不需要挂载数据文件
* 必须启动执行：ENTRYPOINT && CMD train|submission|train_submission, 可以参考Dockerfile
* 容器启动后不可以访问外部网络`--network none`
* 参赛选手需自行创建和参赛英文队名(中文名称转拼音)一致的项目工程(`APP`变量名称，默认*demo*)名称。 项目名需去掉空格和标点符号，只包含小写字母、数字、下划线

## docker mnt 目录说明

### 代码结构
* /data：数据挂载目录,可以通过 `export DATA_DIR` 修改默认挂载
    - train:训练数据(不需要打包进入img,组织方真实数据挂载)
    - eval:评估数据(不需要打包进入img,组织方真实数据挂载)
    - output:评估输出目录(不需要打包进入img,组织方从此目录导出数据)
* /opt
    - app:选手项目地址
      - run.sh：启动文件

```
/
├── data
│   ├── train
│   │   ├── part_1
│   │   │   ├── context.parquet
│   │   │   ├── item.parquet
│   │   │   └── user.parquet
│   │   │── part_2
│   │   ├── ...
│   │   └── raw.parquet
│   ├── eval
│   │   ├── context.parquet
│   │   ├── item.parquet
│   │   └── user.parquet
│   └── output
│       └── result_xxx.csv
└── opt
    └───app
        ├── README.md
        └── run.sh 
```

### 构建命令
#### 创建镜像
根据实际情况修改`Makefile`文件中的参数`APP` `RELEASE`
```
make 
```
#### 使用docker 运行项目
```
make run
```
#### 导出docker img
```
make save
```
