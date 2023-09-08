cd /python/Savya/EmailVerification

# To Start Pending verification
cd Pending_Verification/
kill -9 $(cat Process.txt)
rm -rf *.txt __pycache__/
python3 emailVerification.py & 
echo $! > Process.txt

# To Start False verification
cd ../False_Verification/
kill -9 $(cat Process.txt)
rm -rf *.txt __pycache__/
python3 false_email_verifier.py & 
echo $! > Process.txt

# To Start Creation Operation
cd ../Email_Creator/
kill -9 $(cat Process.txt)
rm -rf *.txt __pycache__/
python3 Email_Creator.py & 
echo $! > Process.txt