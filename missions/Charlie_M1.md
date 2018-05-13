**_Charlie_**
## Mission 1 : Establishing Classical Communication
*70 minutes of gameplay [70/200 points]*

As a security company which mainly focuses on spying on the technologies of other companies, you obtain an intel from your informant that Alice and Bob is developing a new communication channel based on old TV remotes.

The company Alice and Bob have quite a reputation, and you want to figure out whether their technologies are reliable (or even secure). Thanks to his expertise, your informant manages to copy over the necessary tecnical documents. The aim of this mission is to understand what Alice and Bob are up to (by developing the same technology on your own), and then try to see whether there is a way to spy onto their channel.

This mission is divided into smaller tasks, which consists of compulsory and optional tasks. The compulsory tasks are marked with either [Checkpoint], [Final Task], or [Secret Task] flags, while the unmarked tasks are sort of optional. It is thus a priority to complete all the flagged tasks before the optional tasks, as one will not be able to revisit these tasks after the deadline. The compulsory tasks are very important for the upcoming missions. It is also highly advisable to split the tasks among your teammates.

#### [10 points] BREAK the ice, STOMP the ground, LIFT the air
> *This is sort of compulsory, but only to get the group going :P*

Objectives:
1. Choose a team captain,
1. Write down a short company manifesto, and
1. Take a team photo.

Point allocation scheme:
* [Full] points upon completion of the objectives.

#### [30 points] [Checkpoint] Without the electronics, there is NONE
> *Resistor: I'm gonna ask you this one time, where is the circuit?*

> *Transistor: Yeah, I'll do you one better, WHO is the circuit?*

> *Diode: I'll do YOU one better, WHY is the circuit?*

> *- 1 divided by 0*

Objective: Construct two circuits, one capable of sending IR signals, and one capable of receiving IR signals. This means, you need to emulate both Alice and Bob. The objective is accomplished when Charlie-sender (Alice) successfully sends (and Charlie-receiver (Bob) successfully receives) the blinking signal.

Hint: You will need to refer to the technical documents. **It is very important to read all the safety precautions in the documents, as there is a chance that you might burn some electrical components, or even the arduino board. Please be careful!**

Notes:

1. Charlie-sender and Charlie-receiver needs to be perfomed on **two separate arduino boards**, although it is okay to use either one or two computers. Note that with one computer, the two arduino will show up as two different serial ports, so you will need to keep track which one is which.
1. To not raise any suspicion on your identity as a spy to Alice and Bob, it is highly advisable to block your generated IR signals, i.e. don't let Alice and Bob detect IR signals other than theirs. This is particularly important since the IR light is pretty strong and can bounce off the walls of the room a few times, even though it is invisible to your eyes. The gamemaster will provide you with some optical-blocking boxes to cover up your experiments.

Point allocation scheme:
* [Full] points upon correct, efficient, and stable implementation of the circuits, or
* [80%] of total points upon successful implementation of the circuits, but not necessarily correct, efficient, nor stable.

#### [10 points] Asymmetrical cryptography handout
> *When cryptography is outlawed, bayl bhgynjf jvyy unir cevinpl.*

> *-  John Perry Barlow*

Objective: Complete the "asymmetrical cryptography handout". No cheating or copying with Eve allowed [insert stern warning].

Point allocation scheme:
* Based on the number of correct responses in the handout.

#### [20 points] [Final Task] Let make them chat
> *The Internet: transforming society and shaping the future through chat.*

> *- Dave Barry*

Objectives:
1. Successfully communicate a message from Charlie-sender to Charlie-receiver via the IR link by using the program chatting.py,
1. Chatting (i.e. send a few messages back and forth) by using the program chatting.py.

Point allocation scheme:
* [Full] points by completing all the objectives **within 60 minutes** from the start of Mission 1 (leaving 10 more minutes to wrap up other tasks), or if fails,
* [80%] of total points by completing all the objectives within the time limit, or if fails,
* Maximum of [80%] of total points, proportional to the effort and the number of completed tasks at the end of the time limit.
