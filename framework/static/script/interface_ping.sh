`wget -t 1 -T 500 --spider -o ping_data_log ${url}`
count=`cat ping_data_log | grep "200 OK" | wc -l`
if [ $count -gt 0 ]; then
    echo "0"
else
    echo "-1"
fi
