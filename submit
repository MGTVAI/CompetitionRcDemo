# 一、资料list

| 文件 | 说明 |是否必要  |
| --- | --- | --- |
| ${TEAM_NAME}_${version}.img.gz | docker 镜像导出文件 | 是 |
| docker-compose.yml | docker 运行配置，默认使用官方demo中的文件 | 否 |
| resource.md | 资源说明，如果未提交默认按8核32G配置 | 否 |
| how.md or how.ipynb | 代码说明、解题思路,帮助代码审核 | 是 |
| team.md | 团队名称、成员,最高成绩,方便有问题时及时联系 | 是 |

整体打包为单一上传文件 ${TEAM_NAME}_${version}.tar.gz, 在平台网站通过提交评分文件相同的方式使用oss 上传提交(相关上传限制将在6.15号12点放开限制)

# 二、docker 配置说明
### 建议参考使用官方demo 下的三个文件
* `Dockerfile`：docker 打包配置文件，包括基础包、代码导入、依赖安装、命令入口等(`注意不需要打包数据文件`)
* `docker-compose.yml`：docker 镜像运行配置(可以不用上传,有默认配置)，赛事方将运行命令 `docker-compose  run  ${image}`, 选手需要保证容器内的代码能依次执行特征工程、模型训练推理，产生与提交b榜最高成绩基本一致的结果文件 在`/data/output/xxx.csv`
* `Makefile`:参考打包流程，参赛可以参考生成镜像文件,依次执行`打包docker`,`导出docker` 命令（对应`make build`,`make save`)，即可生成对应的docker 镜像导出文件

#### `Dockerfile` 简单说明
```
FROM python:3.6.10       #基础镜像
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime        #时区
COPY . /opt/app       #代码拷贝进镜像
WORKDIR /opt/app
RUN pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r requirements.txt #依赖安装
ENTRYPOINT ["/bin/bash", "/opt/app/run.sh"] #入口
CMD ["train"] #启动参数，默认是生成 可以是train |notebook 等等选手可以添加的需要的启动参数，比如可以可以直接通过镜像运行notebook
```

#### 代码结构
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


## 特别注意点
* 不需要打包官方提供的数据文件，数据文件将在运行时由赛事方按目录规则挂载
* 有资源特别需求的在 `resource.md` 中特别注明，默认将使用8核32G配置
* 运行时建议选手固定各个random 的初始种子值(如 `np.random.seed()`, `torch.manual_seed()`, `torch.backends.cudnn.deterministic`等)，保障运行结果是确定的
* 运行时docker 容器不可以使用任何网络资源
* 选手要保障整体流程在12个小时内运行完成，未完成的成绩无效

# 三、resource.md
样例说明

| 资源 | 需求 | 备注 |
| --- | --- | --- |
| 内存 | 32G | 最高256G |
| cpu | 8核 | 最高32核 |
| 磁盘 | 50G | 磁盘需求，默认数据盘挂载在/data |
| gpu | 2080Ti 单卡，显存12G | 可以使用2080Ti 或 v100 |
|cuda | cuda10.1-cudnn7| 比如使用基础镜像 `pytorch/pytorch:1.3-cuda10.1-cudnn7-deve`， 配置文件 `docker-compose.yml` 需添加运行 `runtime: nvidia`|

# 四、 how.md
代码与思路说明文件，帮助比赛方审核，选手应保障代码的审计思路明晰，内容应该包括：
* 每个目录、每个文件的用途说明
* 基本特征工程 字段说明
* 使用的模型及框架介绍
* 流程说明及对应代码位置

# 五、team.md
团队说明

| 项 | 值 | 备注 |
| --- | --- | --- |
|团队名称| xxx|排行榜上的名称|
|最高成绩| xx| 最高成绩|
|最高成绩提交时间| ||
|队长信息| xxx，|真实姓名、网站注册用户名、手机号码、邮箱|
|队员1 | xxx，|真实姓名、网站注册用户名、手机号码、邮箱|
|队员2 | xxx，|真实姓名、网站注册用户名、手机号码、邮箱|



