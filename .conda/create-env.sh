SCRIPT_DIR=$(dirname "$0")
RETURN_DIR=$(pwd)
cd $SCRIPT_DIR
SCRIPT_DIR=$(pwd)
cd $RETURN_DIR
ENV_NAME=$(echo $(basename $(dirname $SCRIPT_DIR)) | awk '{print tolower($0)}')

YAML_PATH=$SCRIPT_DIR/environment.yaml
ENV_PATH=$SCRIPT_DIR/envs/$ENV_NAME

CONDA_CMD="conda env create -f $YAML_PATH -p $ENV_PATH"

echo $CONDA_CMD

eval $CONDA_CMD
