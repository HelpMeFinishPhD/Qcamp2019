**_Bob 2 (Eve)_**
## Mission 2 : Eavesdropping Quantum Keys
*90 minutes of gameplay [60/200 points]*

Your evil mastermind seems to work out. Thanks to your professional team mate, you now have a direct connection (splitted) from Alice's photons. You can look at her polarisation choices. At the same time, you have made some deal with Charlie. Things are just going to get better **The aim of this mission is to perform a photon number splitting attack, analyse your measurement results, and determine the secure key.**

This mission is divided into smaller tasks, which consists of compulsory and optional tasks. The compulsory tasks are marked with either [Checkpoint], [Final Task], or [Secret Task] flags, while the unmarked tasks are sort of optional. It is thus a priority to complete all the flagged tasks before the optional tasks, as one will not be able to revisit these tasks after the deadline. The compulsory tasks are very important for the upcoming missions. It is also highly advisable to split the tasks among your teammates.

#### [20 points] [Checkpoint] Distinguish Alice's polarisation states
> *We live in a very insecure world with a very insecure communications platform.*

> *- John McAfee*

Objectives:
1. Intercept some of Alice's photons. Successfully perform polarisation projection measurements on Alice's photons using two photodetectors.
2. Analyse the signals from both photodetectors and associate the correct polarisation state to each signal.


Point allocation scheme:
* [Full] points after completion of the mission

Step by step walkthrough:

1. Run `key_logger.py` to intercept the unsifted key sent from Alice to Bob through the quantum channel. (Notice how Alice's signal is intercepted through the use of the beamsplitter.)

2. Run `runInterceptor.py` to analyse the unsifted key.

* First, load the file using the dropdown list and click `Start`.

* A plot of the Signal 1 vs. Signal 2 should display groups of data. The grouping is already done using cluster analysis. The groups are arbitrarily assigned the labels `A`, `B`, ..., `E`.

* Correctly match the labels `A`, `B`, ..., `E` to the polarisation states `Horizontal`,`Vertical`,...,`Anti-diagonal`. Click `decode` to convert the signal voltages to polarisation states.

* (Note that at this point, we only decoded for the polarisation states sent through the quantum channel, and have not arrived at the final secret key - for that we will need the choice of polarisation basis sent through the classical channel.)
<br><br>

#### [10 points] Pattern Recognition's handout

Objective: Complete the `Pattern Recognition` handout. No cheating or copying with Charlie allowed.

Point allocation scheme:
* Based on the number of correct responses in the handout.
<br><br>

#### [10 points] Randomness handout
> *Creativity is the ability to introduce order into the randomness of nature.*

> *-  Charles Bennett and Gilles Brassard*

Objective: Complete the `Randomness` handout. No cheating or copying with Charlie allowed.

Point allocation scheme:
* Based on the number of correct responses in the handout.
<br><br>

#### [20 points] [Final Task] Eavesdrop the secret key
> *No one, including me, can totally rule out data surveillance. That's why I write my text messages and emails so that they stand up to being read.*

> *- Frank-Walter Steinmeier*

Objective: By using the spying tools developed in the checkpoint task, eavesdrop the secret key sent by Alice to Bob (there will be a total of 4 keys). The `GameMaster` will guide Alice and Bob in the process of sending key, so listen to the `GameMaster` on when to listen. For each attempt, you need to write down your predictions (max 6 predictions) in a piece of paper, before the `GameMaster` announces it. Your facilitator will help you in validating the keys.

Point allocation scheme:
* [Full] points by successfully and correctly eavesdropping all the secret keys, or
* Maximum of [100%] of total points, proportional to the number of corrrectly eavesdropped keys.
