#! /bin/bash

# This is a demo script that calls gradeMipsSubmission.py to run
# students' MIPS programs.


if [ ! -e grades_q5.csv ]; then
    echo "NetID, Grade, Reason, \"Additional Reason\", \"Date String\", \"Date (seconds)\"" >> grades_q5.csv
fi

for netid in `cat netids`; do
    gradeReason=`./gradeMipsSubmission.py Submissions/$netid/fibonacci.s`

    exitCode=$?
    if [ $exitCode = 0 ]; then
        echo "$netid,$gradeReason,,`date`,`date +%s`"
        echo "$netid,$gradeReason,,`date`,`date +%s`" >> grades_q5.csv
    else
        echo
        echo "$netid,$gradeReason"
        echo -e "$gradeReason" > /tmp/grade.s
        echo >> /tmp/grade.s
        cat Submissions/$netid/fibonacci.s >> /tmp/grade.s

        emacs -nw /tmp/grade.s

        echo -ne "$netid:\tAdditional reason? ";
        read reason;
        echo -ne "$netid:\tGrade? ";
        read grade;

        echo "$netid,$grade,$gradeReason,\"$reason\",`date`,`date +%s`" >> grades_q5.csv
    fi
done

