# this scripts is used to set environments variables 
# for developpers using virtualenv (and not docker)
# Important: You need to source it, not run it !

# just parse the .env and export it's variables
var_names=$(cat .env| grep -v "^#" | grep -v "^\s*$" | cut -d = -f 1)
readarray -t vars_array <<< "$var_names"
source .env
export ${vars_array[@]}

