**_Alice 2 (Charlie)_**
## Mission 2 : Eavesdropping Classical Messages
*90 minutes of gameplay [60/200 points]*

By now you would have established quite a reputation in the communication industry. Some people know that you have some expertise in IR communication, and would like to have some conversation with you.

> *If I offer you quite a handsome sum of money, would you like to hack it?*

And that is it. Now you are the spying company. At some point in time, you overheard that some secretive agent wants to transmit some highly classified information between Alice and Bob. **The aim of this mission is to tap into the communication between Alice and Bob, and obtain the super secret message.**

This mission is divided into smaller tasks, which consists of compulsory and optional tasks. The compulsory tasks are marked with either [Checkpoint], [Final Task], or [Secret Task] flags, while the unmarked tasks are sort of optional. It is thus a priority to complete all the flagged tasks before the optional tasks, as one will not be able to revisit these tasks after the deadline. The compulsory tasks are very important for the upcoming missions. It is also highly advisable to split the tasks among your teammates.

#### [20 points] [Checkpoint] Tap into the channel
> *We live in a very insecure world with a very insecure communications platform.*

> *- John McAfee*

Objective: By using IR receivers installed in different spying locations, look into what Alice is sending to Bob. Mission is accomplished if Charlie can read whatever Alice saying.

Point allocation scheme:
* [Full] points after completion of the mission

Step by step walkthrough:
1. Install the IR receiver, point it to Alice's IR sender, and put it into the listening mode, i.e. by using program `recv_message.py`. Alternatively, you might also want to try the program in `4_HackTools/ClassicalListener/listener.py`, which will listen to everything that is being sent through (not only messages with `[STX]` header and `[ETX]` footer).
1. You might want to install another IR receiver, just in case the first one fails.

#### [10 points] Xi Jie's handout
> *Blah blah bluh.*

> *- Xi Jie*

Objective: Complete the `Xi Jie's` handout. No cheating or copying with Eve allowed [insert stern warning].

Point allocation scheme:
* Based on the number of correct responses in the handout.
<br><br>

#### [10 points] Controlling IR devices handout
> *I could tell my parents hated me. My bath toys were a toaster and a radio.*

> *- Rodney Dangerfield*

Objective: Complete the `Controlling IR Devices` handout. No cheating or copying with Eve allowed [insert stern warning].

Point allocation scheme:
* Based on the number of correct responses in the handout.
<br><br>

#### [20 points] [Final Task] Eavesdrop the secret message
> *No one, including me, can totally rule out data surveillance. That's why I write my text messages and emails so that they stand up to being read.*

> *- Frank-Walter Steinmeier*

Objective: By using the spying tools developed in the checkpoint task, eavesdrop the secret messages sent by Alice to Bob (there will be a total of 4 messages). The `GameMaster` will tell you when the secret messages are being sent. After receiving all the message, **write it down** in the **super secret document** and pass it to the `GameMaster` after the conclusion of the mission.

Point allocation scheme:
* [Full] points by successfully and correctly eavesdropping all the secret message, or
* Maximum of [100%] of total points, proportional to the number of corrrectly eavesdropped messages.
