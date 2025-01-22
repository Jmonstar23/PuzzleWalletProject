#!/bin/zsh

# Prompt for user input
echo "Please enter the path to the file:"
read file

# Sanity check to ensure the file exists
if [[ ! -f $file ]]; then
    echo "Error: File does not exist or is not a regular file."
    exit 1
fi

# Initialize arrays
locked_words=()
varWrds=()
secondary_variable_words=()
marked_words=()
combinations=()

# Read the file line by line
while IFS= read -r line; do
    if [[ $line =~ ^[0-9]+\.\  ]]; then
        # Line starts with a number followed by a period and a space
        index=${line%%.*}
        word=${line#*. }
        locked_words[$index]=$word
    elif [[ $line =~ ^\<.*\>$ ]]; then
        # Line is enclosed in angle brackets
        word=${line#<}
        word=${word%>}
        secondary_variable_words+=("$word")
    elif [[ $line =~ ^# ]]; then
        # Line starts with a hashtag
        word=${line#\#}
        marked_words+=("$word")
    else
        # Line contains only alphanumeric characters
        varWrds+=("$line")
    fi
done < $file

# Function to generate permutations of an array
permute() {
    local items=("$@")
    echo "Permute called with items: ${items[@]}" >&2
    if [[ ${#items[@]} -eq 1 ]]; then
        echo "Base case reached with item: ${items[0]}" >&2
        echo "${items[0]}"
    else
        for ((i=0; i<${#items[@]}; i++)); do
            local remaining=("${items[@]:0:$i}" "${items[@]:$((i+1))}")
            echo "Remaining items: ${remaining[@]}" >&2
            for perm in $(permute "${remaining[@]}"); do
                echo "Perm: ${items[i]} $perm" >&2
                echo "${items[i]} $perm"
            done
        done
    fi
}

# Generate all permutations of variable words
echo "Generating permutations of variable words..."
combinations=($(permute "${varWrds[@]}"))
echo "Permutations generated."

# Generate all pairs of secondary variable words
secondary_combinations=()
for ((i=0; i<${#secondary_variable_words[@]}; i++)); do
    for ((j=i+1; j<${#secondary_variable_words[@]}; j++)); do
        secondary_combinations+=("${secondary_variable_words[i]} ${secondary_variable_words[j]}")
    done
done

# Create a temporary file to store the results
temp_file=$(mktemp)

# Generate all possible array combinations
for combination in "${combinations[@]}"; do
    for secondary_combination in "${secondary_combinations[@]}"; do
        array=()
        for i in {1..24}; do
            if [[ -n ${locked_words[i]} ]]; then
                array[i]=${locked_words[i]}
            fi
        done
        for word in "${marked_words[@]}"; do
            for i in {12..24}; do
                if [[ -z ${array[i]} ]]; then
                    array[i]=$word
                    break
                fi
            done
        done
        for word in $secondary_combination; do
            for i in {1..24}; do
                if [[ -z ${array[i]} ]]; then
                    array[i]=$word
                    break
                fi
            done
        done
        for i in {1..24}; do
            if [[ -z ${array[i]} ]]; then
                array[i]=$(echo $combination | cut -d' ' -f$((i)))
            fi
        done
        echo "${array[@]}" >> $temp_file
    done
done

# Print the results to the screen and save to a file
cat $temp_file
mv $temp_file "output.txt"
echo "Results have been saved to output.txt"
