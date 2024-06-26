#!/bin/bash

isExecutable(){
    if [[ $# -ne 1 ]]; then
        echo "Nu au fost transmisi suficienti parametri" 
        return 0
    fi
    permisions=$(ls -ld $1| cut -f1 -d" " )
    user=${permisions:3:1}
    if [[ $user != "x" ]]; then 
        echo "Nu aveti drepturi de executie asupra fisierului" 
        return 0
    fi
    return 1  
}

exec 3< expected_output.txt
read_next_line() {
    read -r line_output <&3
    echo "$line_output" 
}

#verificarea fisierului de configurare
if [[ ! -f configuration_file.txt ]]; then 
    echo "Fisierul de configurare nu exista" 
    exit 1
fi

configuration_set=1 
path_app="" 
path_outputFile=""
declare -a inputFiles
declare -a arguments
while read -r line
do
    type=$(echo "$line" |cut -f1 -d":")
    value=$(echo "$line"| cut -f2 -d":")
    if [[ $type == "Path to application" ]]; then 
        if [[ -z $value ]]; then 
            echo "The path to the application is not set."
            configuration_set=0
        else
            path_app=$value
        fi
    fi 

    if [[ $type == "Arguments" ]]; then 
        j=0 
        while read -r line 
        do 
            arguments[$j]=$line
            j=$((j+1))
        done < $value
    fi

    if [[ $type == "Input files" ]]; then 
        j=0
        for word in $value
        do 
            inputFiles[$j]=$word
            j=$((j+1))
        done 
    fi
    if [[ $type == "Expected output files" ]]; then 
        if [[ -z $value ]]; then
            echo "The output expected for the application is not set." 
            configuration_set=0
        else     
            path_outputFile=$value
            echo "The output file is set to $path_outputFile" >/dev/null 
        fi
    fi 
done < configuration_file.txt 


if [[ $configuration_set -eq 0 ]]; then
    echo "Write the configuration file properly" 
    exit 1
fi

isExecutable "$path_app"
response_isExecutable=$?
if [[ $response_isExecutable == 0 ]]; then 
    exit 1
fi 
 

i=1
j=0
passed_test=0
for arg in "${arguments[@]}"
do 
    >test$i.txt
    succes=1
    #time and returned value 
    start_time=$(date +%s.%N)

    if [[ -z $inputFiles ]]; then 
        result=$($path_app $arg 2>errors.txt)
    else 
        result=$($path_app $arg < "${inputFiles[$j]}" 2>errors.txt)
    fi
    
    return_code=$?
    end_time=$(date +%s.%N)
    execution_time=$(echo "scale=3; ($end_time - $start_time) / 1" | bc)
    if (( $(echo "$execution_time < 1" | bc -l) )); then
        execution_time="0$execution_time"
    fi

    #system calls and library calls
    if [[ -z $inputFiles ]]; then 
        strace -o strace_output.txt $path_app $arg >/dev/null 2>/dev/null & 
        strace -e trace=signal -o strace_signals.txt $path_app $arg >/dev/null 2>/dev/null &
        ltrace -o ltrace_output.txt $path_app $arg >/dev/null 2>/dev/null &
        wait 
    else 
        strace -o strace_output.txt $path_app $arg < "${inputFiles[$j]}" >/dev/null 2>/dev/null &
        strace -e trace=signal -o strace_signals.txt $path_app $arg < "${inputFiles[$j]}" >/dev/null 2>/dev/null &
        ltrace -o ltrace_output.txt $path_app $arg < "${inputFiles[$j]}" >/dev/null 2>/dev/null &
        wait
    fi
    j=$((j+1))

    #output
    #execution time 
        echo "$(echo $execution_time | tr '\n' ' ')s" >> test$i.txt
    #errors
    if [[ -s errors.txt ]]; then 
        cat errors.txt >> test$i.txt
        succes=0
    else 
        echo "No errors" >> test$i.txt
    fi

    #created files
    files=$(egrep "^creat" < strace_output.txt | cut -f2 -d"," | tr "\"" " ")
    if [[ -z $files ]]; then 
        echo "No files created" >> test$i.txt
    else  
        echo "$files" >> test$i.txt
    fi

    #returned value
        echo "$return_code" >> test$i.txt

    #comparing the result with the expected output
    line=$(read_next_line)
    if [[ $line = $result ]]; then 
        echo "$line" >> test$i.txt
        echo "$result">>test$i.txt  
    else
        echo "$line" >> test$i.txt
        echo "$result">> test$i.txt 
        succes=0
    fi 

    #print the signals
        echo "Signals:" >> test$i.txt
        cat strace_signals.txt >> test$i.txt

    #print the system calls
        echo "System calls:" >> test$i.txt
        cat strace_output.txt >> test$i.txt

    #print the library calls
        echo "Library calls:" >> test$i.txt
        cat ltrace_output.txt >> test$i.txt
    
    #check if the test is succesful
    if [[ $succes -eq 1 ]]; then 
        echo " Passed" >> test$i.txt
        passed_test=$((passed_test+1))
    else 
        echo " Failed" >> test$i.txt
    fi 
    i=$((i+1))
done
exec 3<&-


i=$((i-1))
succes_rate=$((passed_test*100/i))
>succes.txt
echo "Succes rate: $succes_rate%">>succes.txt