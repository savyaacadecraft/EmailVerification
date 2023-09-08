cd /python/Savya/EmailVerification

# To Stop Pending verification
cd Pending_Verification/
kill -9 $(cat Process.txt)

# To Stop False verification
cd ../False_Verification/
kill -9 $(cat Process.txt)

# To Stop Creation Operation
cd ../Email_Creator/
kill -9 $(cat Process.txt)