# Hashing converts the password into an irreversible string.
Suppose a user registers with:

Username : jayanthi
Password : jayanthi@123
If someone gains access to the database, they immediately know everyone's passwords.
That's a major security risk.

# JWT-->JSON Web Token
It is used to identify a logged-in user.
without JWT,Every request would require:username,password -->again and again

The chatbot makes external LLM API calls, which are I/O-bound operations. I used ThreadPoolExecutor so multiple chat requests can be processed concurrently instead of blocking one another while waiting for the LLM response. Each request still uses the authenticated user's session, so conversations remain isolated."
