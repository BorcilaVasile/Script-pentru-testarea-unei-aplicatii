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

echo "Test started..." 
echo "Configuration file is verified..." 
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

echo "The configuration file is set properly"
echo "Select what you want to see additional:" 
echo "1. Execution time"
echo "2. Errors"
echo "3. Files created"
echo "4. Returned value"   
echo "5. Result" 
echo "6. Signals"
echo "7. System calls"
echo "8. Library calls"
echo "9.None" 
read choice 
if [[ $choice =~ ^[1-9]+$ ]]; then
    # Resetăm toate opțiunile la 0
    show_execution_time=0
    show_errors=0
    show_files=0
    show_returned_value=0
    show_result=0
    show_signals=0
    show_system_calls=0
    show_library_calls=0

    # Verificăm fiecare opțiune selectată în choice
    if [[ $choice == *"1"* ]]; then
        show_execution_time=1
    fi
    if [[ $choice == *"2"* ]]; then
        show_errors=1
    fi
    if [[ $choice == *"3"* ]]; then
        show_files=1
    fi
    if [[ $choice == *"4"* ]]; then
        show_returned_value=1
    fi
    if [[ $choice == *"5"* ]]; then
        show_result=1
    fi
    if [[ $choice == *"6"* ]]; then
        show_signals=1
    fi
    if [[ $choice == *"7"* ]]; then
        show_system_calls=1
    fi
    if [[ $choice == *"8"* ]]; then
        show_library_calls=1
    fi
    if [[ $choice == *"9"* ]]; then
        show_execution_time=0
        show_errors=0
        show_files=0
        show_returned_value=0
        show_result=0
        show_signals=0
        show_system_calls=0
        show_library_calls=0
    fi

else
    echo "Your choice is wrong. All options will be displayed"
    show_execution_time=1
    show_errors=1
    show_files=1
    show_returned_value=1
    show_result=1
    show_signals=1
    show_system_calls=1
    show_library_calls=1
fi
 

i=1
j=0
passed_test=0

for arg in "${arguments[@]}"
do 
    succes=1
    echo " "
    echo -ne "\033[1;4;34mTest $i\033[0m"
    i=$((i+1))
   


    #time and returned value 
    start_time=$(date +%s.%N)

    if [[ -z $inputFiles ]]; then 
        result=$($path_app $arg 2>errors.txt)
        #system calls and library calls
        strace -o strace_output.txt $path_app $arg >/dev/null 2>/dev/null & 
        strace -e trace=signal -o strace_signals.txt $path_app $arg >/dev/null 2>/dev/null &
        ltrace -o ltrace_output.txt $path_app $arg >/dev/null 2>/dev/null &
        wait 
    else 
        result=$($path_app $arg < "${inputFiles[$j]}" 2>errors.txt)
        #system calls and library calls
        strace -o strace_output.txt $path_app $arg < "${inputFiles[$j]}" >/dev/null 2>/dev/null &
        strace -e trace=signal -o strace_signals.txt $path_app $arg < "${inputFiles[$j]}" >/dev/null 2>/dev/null &
        ltrace -o ltrace_output.txt $path_app $arg < "${inputFiles[$j]}" >/dev/null 2>/dev/null &
        wait
    fi
    j=$((j+1))

    return_code=$?
    end_time=$(date +%s.%N)
    execution_time=$(echo "scale=3; ($end_time - $start_time) / 1" | bc)
    if (( $(echo "$execution_time < 1" | bc -l) )); then
        execution_time="0$execution_time"
    fi

   


    #output
    #execution time 
    if (( show_execution_time == 1 )); then 
        echo " " 
        echo -ne "\033[1mExecution time:\033[0m"
        echo " $(echo $execution_time | tr '\n' ' ')s"
    fi

    #errors
    if [[ -s errors.txt ]]; then 
        if (( show_errors == 1 )); then 
            echo " " 
            echo -e "\033[1;31mErrors:\033[0m"
            cat errors.txt
        fi 
        succes=0
    else 
        if (( show_errors == 1 )); then 
            echo " " 
            echo -e "\033[1;32mNo errors\033[0m"
        fi
    fi

    #created files
    files=$(egrep "^creat"<strace_output.txt| cut -f2 -d"," | tr "\"" " ")
    if (( show_files == 1 )); then 
        if [[ -z $files ]]; then 
            echo " " 
            echo -e "\033[1mNo files created\033[0m"
        else  
            echo " "
            echo -e "\033[1mFiles created:\033[0m$files"
        fi
    fi

    #returned value
    if (( show_returned_value == 1 )); then
        echo " " 
        echo -ne "\033[1mReturned value:\033[0m$return_code"
    fi 
    if (( return_code == 0 )); then
        if (( show_returned_value == 1 )); then 
            echo -e "\033[1;32m  CORECT\033[0m" 
        fi
    else
        if (( show_returned_value == 1 )); then 
            echo -e "\033[1;31m  WRONG\033[0m" 
        fi 
        succes=0
    fi

    
    #comparing the result with the expected output
    line=$(read_next_line)
    if [[ $line = $result ]]; then 
        if (( show_result == 1 )); then 
            echo " "
            echo -e "\033[1mExpected value:\033[0m$line"
            echo -ne "\033[1mObtained value:\033[0m"
            if [[ -z $result ]]; then 
                echo -ne "\033[1;31m  NONE\033[0m" 
            else 
                echo -n "$result"
            fi
            echo -e "\033[1;32m  CORECT\033[0m"  
            echo " "
        fi
    else
        if (( show_result == 1 )); then 
            echo " "
            echo -e "\033[1mExpected value:\033[0m$line"
            echo -ne "\033[1mObtained value:\033[0m"
            if [[ -z $result ]]; then 
                echo -ne "\033[1;31m  NONE\033[0m" 
            else 
                echo -n "$result"
            fi
            echo -e "\033[1;31m  WRONG\033[0m" 
            echo " "
        fi
        succes=0
    fi 
     
    
    #print the signals
    if (( show_signals == 1 )); then 
        echo " " 
        echo -e "\033[1mSignals:\033[0m"
        cat strace_signals.txt| head -n 1
    fi

    #print the system calls
    if (( show_system_calls == 1 )); then 
        echo " " 
        echo -e "\033[1mSystem calls:\033[0m"
        cat strace_output.txt| head -n 1
    fi 

    #print the library calls
    if (( show_library_calls == 1 )); then 
        echo " "
        echo -e "\033[1mLibrary calls:\033[0m"
        cat ltrace_output.txt| head -n 1
    fi
    
    #check if the test is succesful
    if [[ $succes -eq 1 ]]; then 
        echo -e "\033[1;32m Passed\033[0m"
        passed_test=$((passed_test+1))
    else 
        echo -e "\033[1;31m Failed\033[0m"
    fi 

done
exec 3<&-

i=$((i-1))
succes_rate=$((passed_test*100/i))
echo " "
echo -e "\033[1mSucces rate: \033[0m$succes_rate%"