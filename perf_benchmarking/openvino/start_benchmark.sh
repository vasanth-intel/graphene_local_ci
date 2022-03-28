#!/bin/bash
echo $PWD
echo $1
echo $2
config=$1
mode=$2
if [ "${config}" = "native" ] && [ "${mode}" = "throughput" ]
then
    cmd="./benchmark_app"
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
fi
if [ "${config}" = "native" ] && [ "${mode}" = "latency" ]
then
    cmd="./benchmark_app"
    export LD_PRELOAD="/usr/local/lib/libmimalloc.so.1.7"
fi
if [ "${config}" = "gramine-direct" ]
then
    cmd="gramine-direct benchmark_app"
fi            
if [ "${config}" = "gramine-sgx" ]
then
    cmd="gramine-sgx benchmark_app"
fi
export PATH=$PREFIX:$PATH
which gramine-sgx
echo "LD_PRELOAD : "
echo $LD_PRELOAD
if [ "${mode}" = "throughput" ]
then
    for ((i=1;i<=1;i++));
    do
        sleep 5
        KMP_AFFINITY=granularity=fine,noverbose,compact,1,0 numactl --cpubind=0 --membind=0 ${cmd} \
        -m ${model} \
        -d CPU -b 1 -t 20 \
        -nstreams $THREADS_CNT -nthreads $THREADS_CNT -nireq $THREADS_CNT 2>&1 | tee throughput_${config}_${i}.txt
    done
fi

sleep 5

if [ "${mode}" = "latency" ]
then
    for ((i=1;i<=1;i++));
    do
        sleep 5
        KMP_AFFINITY=granularity=fine,noverbose,compact,1,0 numactl --cpubind=0 --membind=0 ${cmd} \
        -m ${model} \
        -d CPU -b 1 -t 20 -api sync 2>&1 | tee latency_${config}_${i}.txt
    done
fi

sleep 5