cd /python/Savya/EmailVerification

# To Start Pending verification
kill -9 $(cat Pending_Verification/Process.txt)
python3 Pending_Verification/emailVerification.py & 
echo $! > Pending_Verification/Process.txt

# To Start False verification
kill -9 $(cat False_Verification/Process.txt)
python3 False_Verification/false_email_verifier.py & 
echo $! > False_Verification/Process.txt

# To Start Creation Operation
kill -9 $(cat Email_Creator/Process.txt)
python3 Email_Creator/Email_Creator.py & 
echo $! > Email_Creator/Process.txt