#!/bin/bash
#this is the enterpoint

BIN_DIR=`dirname $0`
cd ${BIN_DIR}

train_base_dir=${DATA_DIR:-/data}
submission_output_dir="${train_base_dir}/output"

function train(){
    # only train the model
    echo "train not implement, call train_submission"
    train_submission
}

function submission() {
    # use trained model to submission 
    echo "submission not implement, call train_submission"
    train_submission
}
function train_submission() {
    train_file="${train_base_dir}/train/part_1/context.parquet"
    test_file="${train_base_dir}/train/part_30/context.parquet"
    submission_input_file="${train_base_dir}/eval/context.parquet"
    mkdir -p "./data/ouput/" #tmp save data and model
    mkdir -p "${submission_output_dir}" #submission output dir
    python base_train.py \
     --train_file=$train_file \
     --test_file=$test_file \
     --submission_input_file=$submission_input_file \
     --model_out="./data/ouput/model_`date +%Y%m%d_%H%M%S`.pkl" \
     --test_out="./data/ouput/test_`date +%Y%m%d_%H%M%S`.data" \
     --submission_out="${submission_output_dir}/submission_`date +%Y%m%d_%H%M%S`.csv" \

}


function check_dir(){
    dirname="$1"
    ! [ -d "${dirname}" ] && echo "dir: '${dirname}' not ok, please check the related" && exit 1
}

function usage(){
 echo '  Usage: ./run.sh train|submission|train_submission'
}

check_dir "${train_base_dir}/train"
check_dir "${train_base_dir}/eval"
case "$1" in
    "train")
        train
        ;;
    "submission")
        submission 
        ;;
    "train_submission")
        train_submission
        ;;
    *)
        usage
        ;;
esac
