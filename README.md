# Description

Demo of a 2FA lock system using an RFID card and face recognition from a camera.
The architecture and the work is described in Report.pdf and the subjet is from Subject.pdf.

# CLI

Allow a manager to add an user to a floor server (need to add the permissions to the DB manually)

# Raspberry

The code running on the Raspberry allowing it to make the 2FA.

# Arduino

Mimicking the lock by powering a led when the door is open.

# Floor server

A server connected to multiples Raspberry and containing a SQL DB each.

# Central server

The server acting as a phone book for the user so he does not have to know which floor server to address for which door.
