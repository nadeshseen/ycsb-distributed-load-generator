sum=0
for FILE in ./splitted_files/*;
do 
var=$(wc -l $FILE | awk '{print $1}'); 
echo $FILE "-" $var
sum=$((sum+var))
done
echo "Sum of all files -" $sum