#!/bin/bash

export INSTALLDIR=/opt/intel/openvino_2021
export OPENVINO_DIR=/opt/intel/openvino_2021
export PATH="$OPENVINO_DIR/deployment_tools/model_optimizer${PATH:+:$PATH}"
export PYTHONPATH="$OPENVINO_DIR/deployment_tools/model_optimizer${PYTHONPATH:+:$PYTHONPATH}"
export InferenceEngine_DIR=/opt/intel/openvino_2021.4.752/deployment_tools/inference_engine/share/
export ngraph_DIR=$INSTALLDIR/deployment_tools/ngraph/cmake
export LD_LIBRARY_PATH=$INSTALLDIR/deployment_tools/ngraph/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export TBB_DIR=$INSTALLDIR/deployment_tools/inference_engine/external/tbb/cmake
export LD_LIBRARY_PATH=$INSTALLDIR/deployment_tools/inference_engine/external/tbb/lib:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export OpenCV_DIR="$INSTALLDIR/opencv/cmake"
export LD_LIBRARY_PATH="$INSTALLDIR/opencv/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH="$INSTALLDIR/opencv/share/OpenCV/3rdparty/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH=/opt/intel/openvino_2021.4.752/deployment_tools/inference_engine/lib/intel64:$LD_LIBRARY_PATH