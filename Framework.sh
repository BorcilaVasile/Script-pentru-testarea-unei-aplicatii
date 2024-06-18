#!/bin/bash

isExecutable(){
    if [[ $# -ne 1 ]]; then
        echo "Nu au fost transmisi suficienti parametri" 
        return 0
    fi
    permisions=$(ls -ld $1| cut -f1 -d" " )
    user=${permisions:3:1}
    group=${permisions:6:1}
    others=${permisions:9:1}
    if [[ $user != "x" ]]; then 
        echo "Nu aveti drepturi de executie asupra fisierului" 
        return 0
    fi
    return 1  
}

echo "Test started..." 
echo "Configuration file is verified..." 

configuration_set=1 
path_app="" 
path_outputFile=""
while read -r line
do
    type=$(echo $line |cut -f1 -d":")
    value=$(echo $line| cut -f2 -d":")
    if [[ $type == "Calea catre aplicatie" ]]; then 
        if [[ -z $value ]]; then 
            echo "The path to the application is not set."
            configuration_set=0
        else
            path_app=$value
        fi
    fi 
    if [[ $type == "Expected output files" ]]; then 
        if [[ -z $value ]]; then
            echo "The output expected for the application is not set." 
            configuration_set=0
        else     
            path_outputFile=$value
        fi
    fi 
done < configuration_file.txt 

if [[ $configuration_set -eq 0 ]]; then
    echo "Rescrie fisierul de configuratie" 
    exit 1
fi

isExecutable $path_app
response_isExecutable=$?
if [[ $response_isExecutable == 0 ]]; then 
    exit 1
fi 

echo "The configuration file is set properly"
echo " "
echo "Test 1"
echo " " 
#test one 
start_time=$(date +%s.%N)
result=$(strace -o strace_output.txt $path_app add 9 2 2>/dev/null & ltrace -o ltrace_output.txt $path_app add 9 2 2>/dev/null &)
return_code=$?
end_time=$(date +%s.%N)
execution_time=$(echo "scale=3; ($end_time - $start_time) / 1" | bc)
if (( $(echo "$execution_time < 1" | bc -l) )); then
    execution_time="0$execution_time"
fi


echo "Valoarea returnată de cod este $return_code"

if (( return_code == 0 )); then 
    echo "CORECT" 
else
    echo "INCORECT" 
fi

echo "Timp de executie: $(echo $execution_time | tr '\n' ' ')s"

read -r line < expected_output.txt
if [[ $line = $result ]]; then 
    echo "Am obtinut valoarea potrivita" 
else
    echo "VALOARE GRESITA" 
    echo "Valoare obtinuta: $result"
    echo "Valoare asteptata: $line"
fi 

echo "Apeluri de sistem capturate:"
cat strace_output.txt| head -n 1
