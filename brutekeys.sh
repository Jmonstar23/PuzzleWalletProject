#!/bin/zsh


Time="$(date -j "+[%H:%M:%S]")"

# Prompt for user input
echo "Please enter the path to the file: "
read file

# Sanity check to ensure the file exists
if [[ ! -f $file ]]; then
    echo "Error: File does not exist or is not a regular file."
    exit 1
fi

echo "\n\n...File found!\n\n"
echo "\n\n...What would you like to name the output?\n\n"
read output

# Initialize arrays
lockdWrds=()
varWrds=()
unsureWrds=()
nonBpi=()
combos=()
alt_combo=()
echo "\n...$Time DEBUG: 6 array variables initialized.../n"
# Read the file line by line
while IFS= read -r line; do
    if [[ $line =~ ^[0-9]+\.\  ]]; then
        # Line starts with a number followed by a period and a space
        index=${line%%.*}
        word=${line#*. }
        echo "$Time DEBUG:[$line] chosen for locked, index [$index] extracted, and [$word] extracted as keyword..."
        lockdWrds[$index]=$word
    elif [[ $line =~ ^\<.*\>$ ]]; then
        # Line is enclosed in pipes
        word=${line#<}
        word=${word%>}
        echo "$Time DEBUG:...[$line] chosen as unsureWrd:[$word] with Markers stripped off..."
        unsureWrds+=("$word")
    elif [[ $line =~ ^\# ]]; then
        # Line starts with a hashtag
        word=${line#\#}
        echo "$Time DEBUG:...[$line] chosen as nonBpi word:[$word] with markers removed..."
        nonBpi+=("$word")
    else
        # Line contains only alphanumeric characters
        echo "$Time DEBUG:...[$line] assigned to varWords array..."
        varWrds+=("$line")
    fi
done < $file
echo "$Time DEBUG: Input file:$file has been processed into appropraite arrays"


# Function to generate permutations of an array
permute() {
    local items=("$@")
#    echo "$Time DEBUG: Permute called with items: ${items[@]}" >&2
    if [[ ${#items[@]} -eq 1 ]]; then
        echo "${items[0]}"
#        echo "Base Reached with item: ${items[@]}" >&2
    else    
        for ((i=0; i<${#items[@]}; i++)); do
            local remaining=("${items[@]:0:$i}" "${items[@]:$((i+1))}")
#           echo "$Time DEBUG: Remaining items: ${remaining[@]}" >&2
            for perm in $(permute "${remaining[@]}"); do            
#            	echo "$Time DEBUG: Perm: ${items[i]} $perm" >&2     	
                echo "${items[i]} $perm"
            done
#           echo "$Time DEBUG: innerloop done" >&2
        done
#        echo "$Time DEBUG: outerloop done" >&2
    fi
    echo "$Time DEBUG: local function completed" >&2
}

# Function to generate permutations of an array iteratively 
# permute() { 
# 	local items=("$@") 
# 	local n=${#items[@]} 
# 	local c=() 
# 	local i 
# 	
# 	for ((i=0; i<n; i++)); do 
# 		c+=0 
# 	done 
# 	
# 	echo "${items[@]}" 
# 	i=0 
# 	while ((i < n)); do 
# 		if ((c[i] < i)); then 
# 			if ((i % 2 == 0)); then 
# 				local temp=${items[0]} 
# 				items[0]=${items[i]} 
# 				items[i]=$temp 
# 			else 
# 				local temp=${items[c[i]]} 
# 				items[c[i]]=${items[i]} 
# 				items[i]=$temp 
# 			fi 
# 			echo "${items[@]}" 
# 			((c[i]++)) 
# 			i=0 
# 		else 
# 			c[i]=0 
# 			((i++)) 
# 		fi 
# 	done 
# }



# Generate all permutations of variable words
echo "$Time DEBUG: assigning array variable combos to results of applying function to varWords array now..."
combos=($(permute "${varWrds[@]}"))

echo "$Time DEBUG:...combos created with function completed...\nCombos:$combos"

# Generate all pairs of alt variable words
alt_combos=()
for ((i=0; i<${#unsureWrds[@]}; i++)); do
    for ((j=i+1; j<${#unsureWrds[@]}; j++)); do
        alt_combos+=("${unsureWrds[i]} ${unsureWrds[j]}")
    done
done

echo "$Time DEBUG:...alt_combos created from unsureWrds array completed...\n\n AltCombos:$alt_combos"

# Create a temporary file to store the results
temp_file=$(mktemp)
echo "$Time DEBUG:...temp file created..."

# Generate all possible array combos
for combo in "${combos[@]}"; do
    for alt_combo in "${alt_combos[@]}"; do
        array=()
        for i in {1..24}; do
            if [[ -n ${lockdWrds[i]} ]]; then
                array[i]=${lockdWrds[i]}
            fi
        done
        for word in "${nonBpi[@]}"; do
            for i in {12..24}; do
                if [[ -z ${array[i]} ]]; then
                    array[i]=$word
                    break
                fi
            done
        done
        for word in $alt_combo; do
            for i in {1..24}; do
                if [[ -z ${array[i]} ]]; then
                    array[i]=$word
                    break
                fi
            done
        done
        for i in {1..24}; do
            if [[ -z ${array[i]} ]]; then
                array[i]=$(echo $combo | cut -d' ' -f$((i)))
            fi
        done
        echo "${array[@]}" >> $temp_file
    done
done

# Print the results to the screen and save to a file
cat $temp_file
mv $temp_file "$output"
echo "Results have been saved to $output"
