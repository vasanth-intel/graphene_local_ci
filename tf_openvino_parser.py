import glob
import os
import pytest
path_bert = os.environ.get('bert_dir')
path_resnet = os.environ.get('resnet_dir')
path_openvino = os.environ.get('openvino_dir')
path = [path_bert , path_resnet , path_openvino]
print ("Path : ", path)

def result_aggregation(input_path):
    all_files = glob.glob(input_path + "/*.txt")
    avg_throughput_native = []
    avg_throughput_gramine_direct = []
    avg_throughput_gramine_sgx = []
    for filename in all_files:
        with open(filename, "r") as f:
            for row in f.readlines():
                row = row.split()
                if row:
                    if "Throughput" in row[0]:
                        throughput = row[1]
                    else:
                        continue
                    if "native" in filename:
                        avg_throughput_native.append(float(throughput))
                    elif "gramine-direct" in filename:
                        avg_throughput_gramine_direct.append(float(throughput))
                    elif "gramine-sgx" in filename:
                        avg_throughput_gramine_sgx.append(float(throughput))
                    else:
                        print("Output file from config list not found.")
    
    return avg_throughput_native, avg_throughput_gramine_direct, avg_throughput_gramine_sgx

def result_aggregation_openvino(input_path):
    all_files = glob.glob(input_path + "/*.txt")
    throughput_native = []
    throughput_gramine_direct = []
    throughput_gramine_sgx = []
    latency_native = []
    latency_gramine_direct = []
    latency_gramine_sgx = []
    for filename in all_files:
        with open(filename, "r") as f:
            for row in f.readlines():
                row = row.split()
                if row:
                    if "Throughput" in row[0] and "throughput" in filename:
                        throughput = row[1]
                    elif "Latency" in row[0] and "latency" in filename:
                        latency = row[1]   
                    else:
                        continue

                    if "native" in filename and "throughput" in filename:
                        throughput_native.append(float(throughput))
                    elif "gramine-direct" in filename and "throughput" in filename:
                        throughput_gramine_direct.append(float(throughput))
                    elif "gramine-sgx" in filename and "throughput" in filename:
                        throughput_gramine_sgx.append(float(throughput))
                    
                    elif "native" in filename and "latency" in filename:
                        latency_native.append(float(latency))
                    elif "gramine-direct" in filename and "latency" in filename:
                        latency_gramine_direct.append(float(latency))
                    elif "gramine-sgx" in filename and "latency" in filename:
                        latency_gramine_sgx.append(float(latency))                        
                    else:
                        continue
    
    return throughput_native, throughput_gramine_direct, throughput_gramine_sgx, latency_native, latency_gramine_direct, latency_gramine_sgx

def display_results(native, direct, sgx):
    if len(native) > 0:
        print("\nNumber of iterations : ",len(native))
        avg_native = sum(native)/len(native)
        print("Throughput values in Native run : ", native, " and average : ", avg_native)        
    if len(direct) > 0:
        avg_direct = sum(direct)/len(direct)
        print("Throughput values in Direct run : ", direct, " and average : ", avg_direct)        
    if len(sgx) > 0:
        avg_sgx = sum(sgx)/len(sgx)
        print("Throughput values in SGX run : ", sgx, " and average : ", avg_sgx)       
    if len(native) > 0 and len(sgx) > 0:       
        print("Degradation Native/SGX : ", (avg_native/avg_sgx))
    if len(native) > 0 and len(direct) > 0:        
        print("Degradation Native/Direct : ", (avg_native/avg_direct))
    if len(direct) > 0 and len(sgx) > 0:        
        print("Degradation Direct/SGX : ", (avg_direct/avg_sgx)) 


class Test_TF_OV_Results():
    @pytest.mark.skipif(path_bert is None,
                    reason="BERT example not executed")    
    def test_bert_workload(self):
        native_result, direct_result, sgx_result = result_aggregation(path_bert)
        display_results(native_result, direct_result, sgx_result)     
        assert(len(native_result) is not None or len(sgx_result) is not None)

    @pytest.mark.skipif(path_resnet is None,
                    reason="RESNET example not executed")    
    def test_resnet_workload(self):
        native_result, direct_result, sgx_result = result_aggregation(path_resnet)
        display_results(native_result, direct_result, sgx_result)        
        assert(len(native_result) is not None or len(sgx_result) is not None)
    
    @pytest.mark.skipif(path_openvino is None,
                    reason="OpenVINO example not executed")    
    def test_openvino_workload(self):
        native_throughput, direct_throughput, sgx_throughput, native_latency, direct_latency, sgx_latency = result_aggregation_openvino(path_openvino)
        print("OpenVINO Throughput results : ")
        display_results(native_throughput, direct_throughput, sgx_throughput)
        print("\nOpenVINO Latency results : ")
        display_results(native_latency, direct_latency, sgx_latency)        
        assert(len(sgx_latency) is not None or len(sgx_throughput) is not None)    